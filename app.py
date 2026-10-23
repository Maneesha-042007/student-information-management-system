from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


# Connect to database
def connect_db():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def init_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL DEFAULT ''
            )
        """)

        # Check whether the email column exists
        columns = [
            row["name"]
            for row in con.execute(
                "PRAGMA table_info(students)"
            ).fetchall()
        ]

        if "email" not in columns:
            con.execute("""
                ALTER TABLE students
                ADD COLUMN email TEXT NOT NULL DEFAULT ''
            """)


# Initialize database
init_db()


# HOME PAGE
@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Student Information Management System</h1>
    <p>Flask server is working!</p>
    <a href="/students">View All Students</a>
    """


# GET: View all students
@app.route("/students", methods=["GET"])
def get_students():
    with connect_db() as con:
        students = con.execute(
            "SELECT id, name, department, email FROM students"
        ).fetchall()

    return jsonify([dict(student) for student in students]), 200


# GET: View one student
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    with connect_db() as con:
        student = con.execute(
            """SELECT id, name, department, email
               FROM students WHERE id = ?""",
            (id,)
        ).fetchone()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student)), 200


# POST: Add a student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a valid JSON object"
        }), 400

    name = data.get("name", "")
    department = data.get("department", "")
    email = data.get("email", "")

    if not all(isinstance(v, str)
               for v in (name, department, email)):
        return jsonify({
            "error": "Name, department and email must be text"
        }), 400

    name = name.strip()
    department = department.strip()
    email = email.strip()

    if not name or not department or not email:
        return jsonify({
            "error": "Name, department and email are required"
        }), 400

    try:
        with connect_db() as con:
            cursor = con.execute(
                """INSERT INTO students
                   (name, department, email)
                   VALUES (?, ?, ?)""",
                (name, department, email)
            )
            student_id = cursor.lastrowid

        return jsonify({
            "message": "Student added successfully",
            "id": student_id,
            "name": name,
            "department": department,
            "email": email
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists. Use a new email."
        }), 409
# PUT: Update a student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a valid JSON object"
        }), 400

    name = data.get("name", "")
    department = data.get("department", "")
    email = data.get("email", "")

    if not all(
        isinstance(value, str)
        for value in (name, department, email)
    ):
        return jsonify({
            "error": "Name, department and email must be text"
        }), 400

    name = name.strip()
    department = department.strip()
    email = email.strip()

    if not name or not department or not email:
        return jsonify({
            "error": "Name, department and email are required"
        }), 400

    with connect_db() as con:
        cursor = con.execute(
            """UPDATE students
               SET name = ?, department = ?, email = ?
               WHERE id = ?""",
            (name, department, email, id)
        )

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

    return jsonify({
        "message": "Student updated successfully",
        "id": id,
        "name": name,
        "department": department,
        "email": email
    }), 200


# DELETE: Delete a student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    with connect_db() as con:
        cursor = con.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

    return jsonify({
        "message": "Student deleted successfully",
        "id": id
    }), 200
# STUDENT REGISTRATION
@app.route("/register", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not department or not email:
            return "All fields are required", 400

        with connect_db() as con:
            cursor = con.execute(
                """INSERT INTO students (name, department, email)
                   VALUES (?, ?, ?)""",
                (name, department, email)
            )

        return (
            f"Registration successful! Student ID: {cursor.lastrowid}"
        )

    return render_template("register.html")


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)