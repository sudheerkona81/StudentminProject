
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from db_config import DB_CONFIG

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def home():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"].strip()
    age = request.form["age"]
    course = request.form["course"].strip()

    if not name or not age or not course:
        return "Please fill in all fields.", 400

    try:
        age = int(age)
        if age < 1 or age > 120:
            return "Please enter a valid age.", 400
    except ValueError:
        return "Age must be a number.", 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
        (name, age, course)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
