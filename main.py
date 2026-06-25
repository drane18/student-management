# Student Management System
#Modified: Student Management System with validation, exception handling, CSV export, Tkinter GUI, and password hashing.

import csv # This module helps us export student records into a CSV file, which can be useful for data analysis or backup purposes.
import re # This module helps us checks whether an email looks valid or not.
import tkinter as tk # This module gives us the main TKinter GUI tools to create windows, buttons, and other GUI elements.
from tkinter import filedialog, messagebox, ttk # These TKinter helpers create dialogs popups, and table views for better user interaction.

import bcrypt # This module helps us exoprt student records into a CSV file.
import mysql.connector #This library connect Python with MySQL.
from mysql.connector import Error, IntegrityError #These classes help use handle MySQL errors cleanly.


EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" #This regex pattern will check whether an email looks valid or not.


#Input Validation.
#Adding new function validate_student_input to validate user input when adding or updating a student record.
def validate_student_input(name, age, email, course): #This function validates all student form values.
    errors = [] #This list stores every validation error message that we encounter during the validation process.
    if not name: #This checks whether the name is empty.
        errors.append("Name cannot be empty.") #This add a name error message.
    elif len(name) < 2: #This checks whether the name is too short.
        errors.append("Name must be at least 2 characters long.") #This add a name length error message.

    try: #This block tries to convert age into a number.
        age_int = int(age) #This will convert the age value into an integer.
        if age_int < 1 or age_int > 120: #This checks whether the age is inside a realistic range.
            errors.append("Age must be between 1 and 120.") #This adds an age range error message.
    except (TypeError, ValueError): #This block runs if age is blank or not a number.
        errors.append("Age must be a number.") #This adds an age error message.
        age_int = None

    if not email: #This checks whether the email is empty.
        errors.append("Email is required.") #This adds an email error message.
    elif not re.fullmatch(EMAIL_PATTERN, email): #This checks whether email matches the email pattern.
        errors.append("Email format is invalid.") #This adds an invalid email error message.
    elif len(email) > 100: #This checks whether the email is too long for the database column.
        errors.append("Email must be 100 characters or less.") #This adds an email length error message.

    if not course: #This checks whether the course is empty.
        errors.append("Course is required.") #This adds a course error message.
    elif len(course) > 100: #This checks whether the course name is too long for the database column.
        errors.append("Course must be 100 characters or less.") #This adds a course length error message.

    is_valid = len(errors) == 0 #This becomes True only when there are no validation errors.
    return is_valid, errors, name, age_int, email, course #This returns validation results and cleaned values.





#Get Students
#Here i first get all student records from the database, then I write those records into a CSV file using the csv module.
def get_students(search_text=""): #This function gets all students or filtered students.
    conn = None #This variable will store the database connection.
    cursor = None #This variable will store the database cursor.
    try: #This block tries to read students records.
        conn = get_connection() #This open the database connection.
        cursor = conn.cursor(dictionary=True) #This returns each row as a dictionary instead of a tuple.
        query = "SELECT id, name, age, email, course FROM students" #This SQL selects columns in the exact order we want for CSV.
        params = () #This tuple stores SQL values for safe query execution.
        search_text = str(search_text).strip() #This removes extra spaces from the search text.
        if search_text: #This checks whether the user typed a search value.
            query += " WHERE name LIKE %s OR email LIKE %s OR course LIKE %s" #This adds search conditions to the SQL query.
            search_value = f"%{search_text}%" #This allows MySQL to match text anywhere in the field.
            params = (search_value, search_value, search_value) #This sends the same search value to all three fields (name, email, course).
        query += " ORDER BY id" #This sorts students by ID.
        cursor.execute(query, params) #This executes the SELECT quesry safely with parameters.
        records = cursor.fetchall() #This fetches all matching student rows into a list of dictionaries.
        return True, records #This returns the students records
    except Error as err: #This block runs if the database read fails.
        return False, f"Database error while reading students: {err}" #This rerturns a readable error message.
    finally: #This block always runs after try or except.
        if cursor:
            cursor.close()
        if conn:
            conn.close() 



# Database connection configuration
def get_connection():
    conn = mysql.connector.connect( #This function will establish a connection to the MySQL database using the provided configuration parameters 
    host="localhost", #This is the my localhost machine where, i runned mysql server 
    user="root", #This is the username for mysql server, by default it is root
    password="Nokia@iphone4", #This is the password for mysql server, we change it also in mysql workbench
    database= "student_management" #This is the database i created in mysql workbench
    )
    return conn #This will return the connection object that we can use to interact with the database




#Exceptional Handling
#Modify the existing add_student function to include exception handling for database errors and input validation errors. 
def add_student(name, age, email, course): #This function add one new student to the database.
    is_valid, errors, name, age, email, course = validate_student_input(name, age, email, course) #This validates the student data.
    if not is_valid: #This checks whether validation failed.
        return False, "\n".join(errors) #This returns all validation errors as one message.
    
    conn = None #This variable will store the databse connection.
    cursor = None #This variable will strore the databse connection cursor.
    try: #This block tries to insert the student.
        conn = get_connection() #This will open the database connection.
        cursor = conn.cursor() #This creates a new cursor to run SQL connections.
        query = "INSERT INTO students (name, age, email, course) VALUES (%s, %s, %s, %s)" #This SQL insert one student.
        cursor.execute(query, (name, age, email, course)) #This safely sends the values into SQL query, preventing SQL injection.
        conn.commit() #This saves the insert permanently in the database.
        return True, f"Student '{name}' added successfully!" #This returns a success message with the new student's name.
    except IntegrityError: #This block runs when a unique email already exists in the database.
        return False, f"A student with this email already exists: {email}" #This returns a friendly duplicate email error message.
    except Error as err: #This block runs for other database errors.
        return False, f"Database error while adding student: {err}" #This returns the database error message for debugging.
    finally: #This block always runs after try or except.
        if cursor:
            cursor.close() #Always close cursor to avoid memory leaks.
        if conn:
            conn.close() #Always close connection to free up resources.

    



#View all Students (READ)
def view_students(): #This will retrieve and display all student records from the database.
    conn = get_connection() #will return the database connection object
    cursor = conn.cursor() #Will create a cursor object to execute SQL queries
    cursor.execute("SELECT * FROM students") #SQL query to select all records from the students table
    records = cursor.fetchall() #This will fetch all the records returned by the query and store them in the variable 'records'

    #Using (if Statement) to check if there are any records in the database
    if not records: # type: ignore
        print("No students found in the database.")
    else:
        print(f"\n{'ID':<5} {'Name':<20} {'Age':<5} {'Email':<30} {'Course':<20}") #This will print the header for the student records with proper formatting.
        print("-" * 80) #And this will print a separator line for better readability.
        for row in records: #This will loop through each record in the 'records' variable
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[3]:<25} {row[4]:<20}") #And this will print each student's details in a formatted manner.

    cursor.close() #cursor closed to free up resources
    conn.close() #And this will close the database connection to free up resources.




#Export to CSV
def export_students_to_csv(file_path): #This function exports all students into a CSV file.
    ok, records = get_students() #This reads all student records from the database.
    if not ok: #This checks whether the database read failed
        return False, records #This returns the database error message.
    if not records: #This checks whether there are no student to export.
        return False, "No students found to export." #This returns a friendly message
    
    try: #This block tries to create and write the CSV file.
        with open(file_path, "w", newline="", encoding="utf-8") as csv_file: #This open the CSV file for writing.
            fieldnames = ["id", "name", "age", "email", "course"] #This defines the CSV column names.
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames) #This creates a CSV writer for dictionaries.
            writer.writeheader() #This writer the first row with column names.
            writer.writerows(records) #This writer all students rows into the CSV file.
        return True, f"Student exported successfully to {file_path}." #This returns a success message.
    except OSError as err: #This block runs if the file connot be written.
        return False, f"File error while exporting CSV: {err}" #This returns the file error.


#Password Hashing(Login System)
def hash_password(password): #This function turns a plain password into a secure hash.
    password_bytes = password.encode("utf-8") #This converts the password string into bytes.
    salt = bcrypt.gensalt() #This creates a random salt for stronger hashing.
    hashed_bytes = bcrypt.hashpw(password_bytes, salt) #This hashes the password with the salt.
    return hashed_bytes.decode("utf-8") #This converts the hash back into a string for MYSQL.

def password_matches(password, password_hash): #This function checks a plain password against a save hash.
    password_bytes = password.encode("utf-8") #This converts the typed password into bytes.
    hash_bytes = password_hash.encode("utf-8") #This converts the saved hash into bytes.
    return bcrypt.checkpw(password_bytes, hash_bytes) #This returns True only when the password matches.

def users_exist(): #This function checks whether at least on login user already exists.
    conn = None #This variable will store the database connection.
    cursor = None #This variable will store the database connection.
    try: # This block tries to count users.
        conn = get_connection() #This opens the database connection.
        cursor = conn.cursor() #This create a cursor to run SQL commands.
        cursor.execute("SELECT COUNT(*) FROM users") #This counts all users in this users table.
        count = cursor.fetchone()[0] #This gets the count number from the first row.
        return count > 0 #This return True when at least one user exists.
    except Error as err: #This block runs if the user tables or database is not ready.
        print(f"Could not check users: {err}") #This prints the database error.
        return False #This return False so setup can continue carefully.
    finally: #This block always runs after try or except.
        if cursor:
            cursor.close()
        if conn:
            conn.close() 

def create_user(username, password): #This function creates a new login user.
    username = str(username).strip() #This removes extra spaces from the username.
    password = str(password) #This makes sure the password is a string.
    if len(username) < 3: #This checks whether the username is too short.
        return False, "Username must be at leats 3 characters." #This returns a username error.
    if len(password) < 6: #This checks whether the password is too short.
        return False, "Password must be at least 6 characters." #This returns a password error.
    
    conn = None #This variable will store the database connection.
    cursor = None #This variable will store that database cursor.
    try: 
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = hash_password(password) #This hashes the password before serving it.
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)" #This SQL inserts one login user.
        cursor.execute(query, (username, password_hash)) #This sends username and hashed password safely.
        conn.commit() #This saves the new user permanertly.
        return True, "User created successfully." #This returns a success message.
    except IntegrityError: #This block runs when the username already exists.
        return False, "Username already exists." #This returns duplicate username message.
    except Error as err: #This block runs for other database errors.
        return False, f"Database error while creating user: {err}" #This returns the database error.
    finally: 
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def login_user(username, password): #This function checks whether login details are correct.
    username = str(username).strip() #This removes extra spaces from the usename.
    password = str(password) #This makes sure the password is a string.
    if not username or not password: #This checks whether either login field is empty.
        return False, "Username and password are required." #This returns a missing input message.
    conn = None
    cursor = None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary = True)
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,)) #This finds the saved hash for the username.
        user = cursor.fetchone() #This gets one matching user row.
        if user is None: #This checks whether the username was not found.
            return False, "Invalid username or password." #This gives a safe generic login error.
        if not password_matches(password, user["password_hash"]): #This checks whether the password is wrong.
            return False, "Invalid username or password." #This gives the same safe generic login error.
        return True, "Login successful." #This returns success when username and password match.
    except Error as err: #This block ruus for database errors.
        return False, f"Database error during login: {err}" #This  returns the database error.
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def setup_first_user_console(): #This function creates the first user from the terminal.
    if users_exist(): #This checks whether a login user already exists.
        return 
    print("\nNo login user found. Create the first admin user.") #This explains why setup is starting.
    while True: #This loop keeps asking until a user is created.
        username = input("Create uername: ") 
        password = input("Create password ")
        ok, message = create_user(username, password) #This tries to save the new user.
        print(message) #And this will prints success or validation error.
        if ok: #Thic checks whether user creation succesded.
            break #And this = leaves the setup loop.



def login_console(): #This function handle terminal login.
    print("\nLogin required.") #This tells the user login is needed.
    for attempt in range(3): #And this will allow three login attempts.
        username = input("Username: ")
        password = input("Password: ")
        ok, message = login_user(username, password)
        print(message) #This prints the login result
        if ok: #This checks whether login succeeded.
            return True # This lets the program continue.
        print(f"Attempt {attempt + 1} failed. Please try again.")

    print("Too many failed login attempts.") #This prints after three failed attempts.
    return False #This stops the program from continuing.




#Update a Student (UPDATE)
def update_student(student_id, name, age, email, course): #This will update a student's information in the database based on the provided student ID.
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE students
               SET name = %s, age = %s, email = %s, course = %s
               WHERE id = %s""" #This SQL query will uodate the student's name, age, email, and course based on the provided student ID.
    cursor.execute(query, (name, age, email, course, student_id)) #This will execute the query with the given parameters, it will replace the placeholders (%s) with the actual values.
    conn.commit() #Commit the transaction to save the changes to the database.
    if cursor.rowcount > 0: #This Will check if any rows were affected by the update query, which indicates that the student was scuccessfully updated.
        print(f"✅ Student ID {student_id} updated successfully!") # Print a success message indicating that the student has been updated.
    else:
        print(f"❌ Student ID {student_id} not found.") #If no rows were affected, it means that the student ID was not found in the database.

    #Close the cursor and connection to free up resources.
    cursor.close()
    conn.close()




#Delete a Student (DELETE)
def delete_student(student_id): #This will delete a student record from the database based on the provided student ID.
    #Here Establish a connection to the database and create a cursor object to execute SQL queries.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,)) # This SQL query will delete the student record from the students table where the id matches the provided student ID.
    conn.commit() #Commit the transaction to save the changes to the database.
    if cursor.rowcount > 0: #This will check if any rows were affectes by the delete query, which indicates that the student was successfully deleted.
        print(f"✅ Student ID {student_id} deleted successfully!") #Print a success message indicating that the student has been deleted.
    else:
        print(f"❌ Student ID {student_id} not found.") #If no rows were affected, it means that the student ID was not found in the database.
    
    #Close the cursor and connection to free up resources.
    cursor.close()
    conn.close()



#Search by name(BONUS)
def search_student(name): #This will search for students in the database based on the provided name.
  #Here Establish a connection to the database and create a cursor object to execute SQL queries.
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{name}%",)) #This SQL query will search for student records in the students table where the name matches the provided name.
  records = cursor.fetchall() #This will fetch all the records returned by the query and store them in the variable 'records'
  for row in records: #This will loop through each record in the 'records' variable
      print(row)
  #Close the cursor and connection to free up resources.
  cursor.close()
  conn.close()





#The main(main loop)
# This will be the main loop of the program where i will display a menu to the user and allow them to choose different option to manage students.
def main():
    while True: #This will create an infinite loop that will keep the program running until the user chooses to exit.
        print("\n ==== Student Management System ====")# This will print the header for the student management system menu.
        print("1. Add Student") #This will print the option to add a student.
        print("2. View All Students") #This will print the option to view all students.
        print("3. Update Student") #This will print the option to update a student.
        print("4. Delete Student") #This will print the option to delete a student.
        print("5. Search Student by Name") #This will print the option to search.
        print("6. Exit") #This will print the option to exit the program.

        choice = input("\nEnter your choice (1-6): ") #This will prompt the user to enter their choice from the new displayed menu


        if choice == "1": #If the user choose option 1, it will execute the code block to add a student.
            name = input("Enter name: ") 
            age = int(input("Enter age: "))
            email = input("Enter email: ")
            course = input("Enter course: ")
            add_student(name, age, email, course) #This will call the add_student function


        elif choice == "2": #If the user choose option 2, it will execute the code block to view all students. 
            view_students() #This will call the view_students function


        elif choice == "3": #If the user choose option 3, it will execute the code block to update a student.
            student_id = int(input("Enter student ID to update: "))
            name = input("Enter new name: ")
            age = int(input("Enter new age: "))
            email = input("Enter new email: ")
            course = input("Enter new course: ")
            update_student(student_id, name, age, email, course) #This will call the update_student funtion


        elif choice == "4": #If the user choose option 4, it will execute the code block to delete a student.
            student_id = int(input("Enter student ID to delete: "))
            delete_student(student_id) #This will call the delete_student function

        
        
        elif choice == "5": #If the user choose option 5, it will execute the code block to search a student by name.
            name = input("Enter name to search: ")
            search_student(name) #This will call the search_student function

        

        elif choice == "6": #If the user choose option 6, it will execute the code block to exit the program.
            print("Exiting the program. Goodbye! 👋")
            break #This will break the infinite loop and exit the program.
        else:
            print("Invalid choice. Please enter a number between 1 and 6.") #If the user enters an invalid choice, it will print an error message prompting them to enter a valid choice.


#TKinter GUI
#Here i created new class StudentApp.
class StudentApp: #This class creates the main TKinter student management window.
    def __init__(self, root): #This method runs when GUI window is created.
        self.root = root #This stores the main window object.
        self.root.title("Student Management Systerm") #This sets the window title.
        self.selected_student_id = None #This stores the currently selected Student ID.
        self.name_var = tk.StringVar() #This stores the name entry value.
        self.age_var = tk.StringVar() #This stores the age entry value
        self.email_var = tk.StringVar() #This store the email entry value.
        self.course_var = tk.StringVar() #This store the course  entry value.
        self.search_var = tk.StringVar() #This store the search entry value.
        self.create_widgets() #This builds all visible GUI widgets.
        self.load_students() #This loads students data into the table.

    def create_widgets(self):# This method creates labels, entries, buttons, and the table. 
        form = ttk.LabelFrame(self.root, text="Student Details") #This creates a titled box for form input.
        form.grid(row=0, column=0, padx=10, pady=10, sticky="ew") #This places the form box at the too.
        ttk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")#This creates the name label.
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5) #This create the name entry.
        ttk.Label(form, text="Age").grid(row=0, column=2, padx=5, pady=5, sticky="w") #This creates the age label.
        ttk.Entry(form, textvariable=self.age_var, width=10).grid(row=0, column=3, padx=5, pady=5) #This creates the age entry.
        ttk.Label(form, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="w") #This creates the email label.
        ttk.Entry(form, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5, pady=5) #This creates the course label.
        ttk.Label(form, text="Course").grid(row=1, column=2, padx=5, pady=5) #This creates the course label.
        ttk.Entry(form, textvariable=self.course_var, width=20).grid(row=1, column=3, padx=5, pady=5) #This creates the course entry.

        buttons = ttk.Frame(self.root)  # This creates a row for action buttons.
        buttons.grid(row=1, column=0, padx=10, pady=5, sticky="ew")  # This places the button row under the form.
        ttk.Button(buttons, text="Add", command=self.add_student_gui).grid(row=0, column=0, padx=5)  # This creates the Add button.
        ttk.Button(buttons, text="Update", command=self.update_student_gui).grid(row=0, column=1, padx=5)  # This creates the Update button.
        ttk.Button(buttons, text="Delete", command=self.delete_student_gui).grid(row=0, column=2, padx=5)  # This creates the Delete button.
        ttk.Button(buttons, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)  # This creates the Clear button.
        ttk.Button(buttons, text="Export CSV", command=self.export_csv_gui).grid(row=0, column=4, padx=5)  # This creates the CSV export button.


        search = ttk.Frame(self.root) #This creates a row for searching.
        search.grid(row=2, column=0, padx=10, pady=5, sticky="ew") #This places the search row under buttons.
        ttk.Label(search, text="Search").grid(row=0, column=0, padx=5, pady=5) #This creates the search label.
        ttk.Entry(search, textvariable=self.search_var, width=35).grid(row=0, column=1, padx=5, pady=5) #This creates the search entry.
        ttk.Button(search, text="Search", command=self.search_students_gui).grid(row=0,column=2, padx=5) #This creates the Search button.
        ttk.Button(search, text="Show All", command=self.load_students).grid(row=0, column=3, padx=5) #This creates the show All button.

        columns = ("id", "name", "age", "email", "course") #This defines the table columns.
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12) #This creates the student table.
        self.tree.grid(row=3, column=0, padx=10, pady=10, sticky="nsew") #This places the table in the window.
        for column in columns: #This loops through each table column.
            self.tree.heading(column, text=column.title()) #This sets the visible heading text.
            self.tree.column(column, width=140) #This sets a default column width.
        self.tree.column("id", width=60, anchor="center") #This makes the ID column narrower.
        self.tree.column("age", width=60, anchor="center") #This makes the age column narrower.
        self.tree.bind("<<TreeviewSelect>>", self.fill_form_from_selection) #This fills the form when a row is selected.
        self.root.columnconfigure(0, weight=1) #This lets the main column expand when the window grows.
        self.root.rowconfigure(3, weight=1) #This lets the table row expand when the window grows.

    def load_students(self): #This method loads all students into the table.
        ok, result = get_students() #This reads all students from the database.
        if not ok: #This checks whether reading failed.
            messagebox.showerror("Database Error", result) #This shows the error in a popup.
            return #This stops the method early.
        self.show_records(result)

    def show_records(self, records): #This methods displays records in the table.
            for item in self.tree.get_children(): #This loops through current table rows.
                self.tree.delete(item) #The removes each old table row.
            for row in records: #This loops through each student record.
                values = (row["id"], row["name"], row["name"], row["email"], row["course"]) #This creates one row of table values.
                self.tree.insert("", "end", values=values) #This inserts the row into the table.





  




 
if __name__ == "__main__":
    main() #This will call the main function to start the program.



            
