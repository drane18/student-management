import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from main import (
    add_student,
    delete_student,
    export_students_to_csv,
    get_students,
    update_student,
)


class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("850x500")

        self.selected_student_id = None
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        form = ttk.LabelFrame(self.root, text="Student Details")
        form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Age").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.age_var, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Course").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(form, textvariable=self.course_var, width=20).grid(row=1, column=3, padx=5, pady=5)

        buttons = ttk.Frame(self.root)
        buttons.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(buttons, text="Add", command=self.add_student_gui).grid(row=0, column=0, padx=5)
        ttk.Button(buttons, text="Update", command=self.update_student_gui).grid(row=0, column=1, padx=5)
        ttk.Button(buttons, text="Delete", command=self.delete_student_gui).grid(row=0, column=2, padx=5)
        ttk.Button(buttons, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)
        ttk.Button(buttons, text="Export CSV", command=self.export_csv_gui).grid(row=0, column=4, padx=5)

        search = ttk.Frame(self.root)
        search.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(search, text="Search").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(search, textvariable=self.search_var, width=35).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search, text="Search", command=self.search_students_gui).grid(row=0, column=2, padx=5)
        ttk.Button(search, text="Show All", command=self.load_students).grid(row=0, column=3, padx=5)

        columns = ("id", "name", "age", "email", "course")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        for column in columns:
            self.tree.heading(column, text=column.title())
            self.tree.column(column, width=140)

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("age", width=60, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.fill_form_from_selection)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

    def load_students(self):
        ok, result = get_students()
        if not ok:
            messagebox.showerror("Database Error", result)
            return
        self.show_records(result)

    def show_records(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in records:
            values = (row["id"], row["name"], row["age"], row["email"], row["course"])
            self.tree.insert("", "end", values=values)

    def add_student_gui(self):
        ok, message = add_student(
            self.name_var.get(),
            self.age_var.get(),
            self.email_var.get(),
            self.course_var.get(),
        )

        if ok:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Error", message)

    def update_student_gui(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Select Student", "Please select a student to update.")
            return

        try:
            update_student(
                self.selected_student_id,
                self.name_var.get(),
                int(self.age_var.get()),
                self.email_var.get(),
                self.course_var.get(),
            )
            messagebox.showinfo("Success", "Student updated successfully.")
            self.clear_form()
            self.load_students()
        except ValueError:
            messagebox.showerror("Invalid Input", "Age must be a number.")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def delete_student_gui(self):
        if self.selected_student_id is None:
            messagebox.showwarning("Select Student", "Please select a student to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Do you want to delete this student?")
        if not confirm:
            return

        try:
            delete_student(self.selected_student_id)
            messagebox.showinfo("Success", "Student deleted successfully.")
            self.clear_form()
            self.load_students()
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def search_students_gui(self):
        ok, result = get_students(self.search_var.get())
        if not ok:
            messagebox.showerror("Database Error", result)
            return
        self.show_records(result)

    def export_csv_gui(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Students CSV",
        )

        if not file_path:
            return

        ok, message = export_students_to_csv(file_path)
        if ok:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def fill_form_from_selection(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        values = self.tree.item(selected_items[0], "values")
        self.selected_student_id = int(values[0])
        self.name_var.set(values[1])
        self.age_var.set(values[2])
        self.email_var.set(values[3])
        self.course_var.set(values[4])

    def clear_form(self):
        self.selected_student_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.email_var.set("")
        self.course_var.set("")
        self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
