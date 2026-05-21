CREATE Database student_management; #

USE student_management; # This command is used to select the database I just created, so that I can create tables and insert data into it.


Create Table students ( 
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    course VARCHAR(100),
    email VARCHAR(100),

);