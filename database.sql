CREATE DATABASE student_management; 

USE student_management; #This command is used to select the database I just created, so that I can create tables and insert data into it.


CREATE TABLE students ( 
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    course VARCHAR(100),
    email VARCHAR(100),

);

CREATE TABLE users (
	id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    salt VARCHAR(64) NOT NULL,
    password_hash VARCHAR(200) NOT NULL 
)
