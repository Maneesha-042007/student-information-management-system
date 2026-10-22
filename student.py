from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to the database
def connect_db():
    return sqlite3.connect("students.db")

# Create the students table
with connect_db() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

# READ: Display all students
@app.route("/")
def home():
    with connect_db() as con:
        students = con.execute(
            "SELECT * FROM students"
        ).fetchall()

    return render_template("register.html", students=students)

# CREATE: Add a student
@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    if not name or not department:
        return "Name and department are required", 400

    with connect_db() as con:
        con.execute(
            "INSERT INTO students (name, department) VALUES (?, ?)",
            (name, department)
        )

    return redirect("/")

# UPDATE: Modify student details
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    if not name or not department:
        return "Name and department are required", 400

    with connect_db() as con:
        con.execute(
            "UPDATE students SET name = ?, department = ? WHERE id = ?",
            (name, department, id)
        )

    return redirect("/")

# DELETE: Remove a student
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    with connect_db() as con:
        con.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )

    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()

        if not name or not department:
            return "Name and Department are required", 400

        conn = sqlite3.connect("students.db", timeout=10)

        try:
            conn.execute(
                "INSERT INTO students (name, department) VALUES (?, ?)",
                (name, department)
            )
            conn.commit()

            return f"""
            <h2>Student Registration Successful</h2>
            <p>Name: {name}</p>
            <p>Department: {department}</p>
            <p>Saved to database successfully!</p>
            """
        finally:
            conn.close()

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)