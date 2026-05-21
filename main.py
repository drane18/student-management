# Student Management System
from webbrowser import get

import mysql.connector

# Database connection configuration
def get_connection():
    conn = mysql.connector.connect( #This function will establish a connection to the MySQL database using the provided configuration parameters 
    host="localhost", #This is the my localhost machine where, i runned mysql server 
    user="root", #This is the username for mysql server, by default it is root
    password="Nokia@iphone4", #This is the password for mysql server, we change it also in mysql workbench
    database= "student_management" #This is the database i created in mysql workbench
    )
    return conn #This will return the connection object that we can use to interact with the database




#ADD a Student(CREATE)
# Let's start adding functions to manage students
def add_student(name, age, email, course): #Here I add a student dataset with the given parameters
    conn = get_connection() #This function will return the database connection object
    cursor = conn.cursor() #This will create a cursor object that I can use to execute SQL queries
    query = "INSERT INTO students (name, age, email, course) VALUES (%s, %s, %s, %s)" #This SQL qeury will insert a new student record into the students table with the provided values.
    cursor.execute(query, (name, age, email, course)) #And this will execute the query with the given parameters, it will replace the placeholders (%s) with the actual values of (name, age, email, and course).
    conn.commit() #This will commit the transaction to the database, which means that the changes will be saved permanently.
    print(f"✅ Student '{name}' added successfully!") #This will print a success message indicating that the student has been added to the database.
    cursor.close() #close the cursor to free up resources
    conn.close() #And this will close the database connection to free up resources.




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
            




if __name__ == "__main__":
    main() #This will call the main function to start the program.



            
