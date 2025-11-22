from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_for_demo_purposes" # Required for flash messages
DATA_FILE = "students.json"

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

@app.route("/", methods=["GET"])
def index():
    students = load_students()
    query = request.args.get("query", "").lower()
    if query:
        students = [s for s in students if query in s["name"].lower() or query in s["roll"].lower()]
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    students = load_students()
    name = request.form["name"]
    roll = request.form["roll"]
    branch = request.form["branch"]
    
    # Simple validation
    if any(s['roll'] == roll for s in students):
        flash(f"Error: Student with Roll No {roll} already exists!", "error")
        return redirect(url_for("index"))

    students.append({"name": name, "roll": roll, "branch": branch})
    save_students(students)
    flash("Student added successfully!", "success")
    return redirect(url_for("index"))

@app.route("/edit/<roll>", methods=["GET", "POST"])
def edit_student(roll):
    students = load_students()
    student = next((s for s in students if s["roll"] == roll), None)

    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        student["name"] = request.form["name"]
        student["branch"] = request.form["branch"]
        save_students(students)
        flash("Student updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", student=student)


@app.route("/delete/<roll>")
def delete_student(roll):
    students = load_students()
    initial_len = len(students)
    students = [s for s in students if s["roll"] != roll]
    
    if len(students) < initial_len:
        save_students(students)
        flash("Student deleted successfully!", "success")
    else:
        flash("Student not found.", "error")
        
    return redirect(url_for("index"))

if __name__ == "__main__":
    import sys
    if 'spyder' in sys.modules:
        app.run(debug=False, use_reloader=False)
    else:
        app.run(debug=True)
