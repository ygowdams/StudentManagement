
from flask import Blueprint, render_template, request, redirect, session
from database import get_db

management_bp = Blueprint("management", __name__)


@management_bp.route("/students")
def students():
    if "student_id" not in session:
        return redirect("/login")

    with get_db() as con:
        records = con.execute(
            "SELECT id, name, email, department FROM students"
        ).fetchall()

    return render_template("students.html", students=records)


@management_bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    if "student_id" not in session:
        return redirect("/login")

    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if name and department:
        with get_db() as con:
            con.execute(
                "UPDATE students SET name=?, department=? WHERE id=?",
                (name, department, id)
            )

    return redirect("/students")


@management_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "student_id" not in session:
        return redirect("/login")

    with get_db() as con:
        con.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
        )

    return redirect("/students")
