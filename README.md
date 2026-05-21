# Student Management System

A simple Student Management System built using Python and MySQL.  
This project performs basic CRUD operations (Create, Read, Update, Delete) for managing student records.

---

## Features

- Add new students
- View all students
- Update student details
- Delete student records
- MySQL database integration

---

## Technologies Used

- Python
- MySQL
- mysql-connector-python

---

## Project Structure

Student-Management/
│
├── student_management.py
├── requirements.txt
├── database.sql
├── README.md
└── .gitignore

---

## Installation

1. Clone the repository

```bash
git clone <your-github-link>
```

2. Install dependencies

```bash
pip3 install -r requirements.txt
```

3. Create database

Run the SQL file in MySQL:

```bash
mysql -u root -p < database.sql
```

4. Run the project

```bash
python3 student_management.py
```

---

## Database

Database Name:

```text
student_management
```

Table Name:

```text
students
```

---

## Author

Digambar Rane