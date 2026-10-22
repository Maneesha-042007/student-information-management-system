import sqlite3

# Connect to the database
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

# CREATE: Insert a student
cursor.execute(
    "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
    ("KKB", "CSSE", "kkb@gitam.com")
)
connection.commit()

print("Student inserted successfully!")

# READ: Retrieve students
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()

for student in students:
    print(student)
cursor.execute(
    "UPDATE students SET department = ? WHERE id = ?",
    ("CSE-AI", 1)
)
connection.commit()

print("Student updated successfully")
cursor.execute(
    "UPDATE students SET department = ? WHERE id = ?",
    ("CSE-AI", 1)
)
connection.commit()

print("Student updated successfully")

connection.close()
