Student Information Management System

A Student Information Management System built using Flask and SQLite. This project provides REST API endpoints to manage student records.

Technologies Used

- Python
- Flask
- SQLite
- HTML
- REST API

Features

- View all students
- View a student by ID
- Add a new student
- Update student details
- Delete a student record
- Store student information in an SQLite database

API Endpoints

Method| Endpoint| Description
GET| "/"| Check server status
GET| "/students"| Get all students
GET| "/students/<id>"| Get a student by ID
POST| "/students"| Add a student
PUT| "/students/<id>"| Update student details
DELETE| "/students/<id>"| Delete a student

How to Run the Project

1. Install Python.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.
4. Install Flask:

pip install flask

5. Run the application:

python app.py

6. Open "http://127.0.0.1:5000/" in your browser.

Project Structure

- "app.py" – Flask application and API routes
- "database.py" – Database connection and setup
- "student.py" – Student data operations
- "crud.py" – CRUD operations
- "templates/" – HTML templates
- "test_post.py" – POST API test
- "test_put.py" – PUT API test
- "test_delete.py" – DELETE API test

Author

Maneesha