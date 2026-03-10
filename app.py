from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "students.db"

def conn():
    return sqlite3.connect(DB)

def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Students(
        student_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        phone TEXT
    )
    """)

    # check if table already has data
    cur.execute("SELECT COUNT(*) FROM Students")
    count = cur.fetchone()[0]

    if count == 0:

        students = [
        (101,'Rahul Sharma','CSE','9876543201'),
        (102,'Sneha Reddy','ECE','9876543202'),
        (103,'Arjun Patel','IT','9876543203'),
        (104,'Priya Singh','CSE','9876543204'),
        (105,'Kiran Kumar','EEE','9876543205'),
        (106,'Anjali Mehta','ECE','9876543206'),
        (107,'Rohit Verma','CSE','9876543207'),
        (108,'Pooja Nair','IT','9876543208'),
        (109,'Vikram Das','MECH','9876543209'),
        (110,'Neha Kapoor','CSE','9876543210'),

        (111,'Amit Gupta','CSE','9876543211'),
        (112,'Divya Iyer','ECE','9876543212'),
        (113,'Sandeep Yadav','EEE','9876543213'),
        (114,'Ritika Shah','IT','9876543214'),
        (115,'Harish Rao','MECH','9876543215'),
        (116,'Kavya Nair','CSE','9876543216'),
        (117,'Manoj Kumar','ECE','9876543217'),
        (118,'Nikita Sharma','IT','9876543218'),
        (119,'Ajay Singh','EEE','9876543219'),
        (120,'Pallavi Das','CSE','9876543220')
        ]

        cur.executemany(
        "INSERT INTO Students VALUES (?,?,?,?)",
        students
        )

    c.commit()
    c.close()

# run database setup
init_db()


@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT COUNT(*) FROM Students")
    total = cur.fetchone()[0]

    cur.execute("SELECT department, COUNT(*) FROM Students GROUP BY department")
    data = cur.fetchall()

    c.close()

    labels = [i[0] for i in data]
    values = [i[1] for i in data]

    return render_template("dashboard.html", total=total, labels=labels, values=values)


@app.route("/students")
def students():
    search = request.args.get("search")
    c = conn()
    cur = c.cursor()

    if search:
        cur.execute("SELECT * FROM Students WHERE name LIKE ?",('%'+search+'%',))
    else:
        cur.execute("SELECT * FROM Students")

    data = cur.fetchall()
    c.close()

    return render_template("students.html", students=data)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":

        sid = request.form["id"]
        name = request.form["name"]
        dept = request.form["dept"]
        phone = request.form["phone"]

        c = conn()
        cur = c.cursor()

        cur.execute("INSERT INTO Students VALUES (?,?,?,?)",
                    (sid,name,dept,phone))

        c.commit()
        c.close()

        return redirect("/students")

    return render_template("add.html")


@app.route("/edit/<id>", methods=["GET","POST"])
def edit(id):

    c = conn()
    cur = c.cursor()

    if request.method == "POST":

        name = request.form["name"]
        dept = request.form["dept"]
        phone = request.form["phone"]

        cur.execute(
        "UPDATE Students SET name=?, department=?, phone=? WHERE student_id=?",
        (name,dept,phone,id)
        )

        c.commit()
        c.close()

        return redirect("/students")

    cur.execute("SELECT * FROM Students WHERE student_id=?",(id,))
    student = cur.fetchone()

    c.close()

    return render_template("edit.html", s=student)


@app.route("/delete/<id>")
def delete(id):

    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM Students WHERE student_id=?",(id,))

    c.commit()
    c.close()

    return redirect("/students")


if __name__ == "__main__":
    app.run(debug=True)