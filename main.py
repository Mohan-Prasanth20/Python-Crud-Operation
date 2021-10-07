from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import cursor

connection = mysql.connector.connect(
    host="localhost", database="Company", user="root", password="Pass@123"
)
app = Flask(__name__)

@app.route("/home")
def home():
    con = connection.cursor()
    sql = "select * from users"
    con.execute(sql)
    result = con.fetchall()
    return render_template("home.html", datas=result)


@app.route("/addusers", methods=["GET", "POST"])
def addusers():

    if request.method == "POST":
        name = request.form["name"]
        phno = request.form["phno"]
        address = request.form["address"]
        bday = request.form["bday"]
        gender = request.form["gender"]
        qualification = request.form["qualification"]
        extraqualifi = request.form["extraqualifi"]
        mycur = connection.cursor()
        sql = "insert into users(name,phno,address,bday,gender,qualification,extraqualifi) values (%s,%s,%s,%s,%s,%s,%s)"
        record = (name, phno, address, bday, gender, qualification, extraqualifi)
        mycur.execute(sql, record)
        connection.commit()
        # mycur.close()
        return redirect(url_for("home"))
    return render_template("addusers.html")


@app.route("/editUsers/<string:id>", methods=["POST", "GET"])
def editUsers(id):
    con = connection.cursor()
    con.execute("SELECT * FROM users WHERE id=%s", [id])
    res = con.fetchone()
    return render_template("editUsers.html", datas=res)


@app.route("/update", methods=["GET", "POST"])
def update():
    con = connection.cursor()
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        phno = request.form["phno"]
        address = request.form["address"]
        bday = request.form["bday"]
        gender = request.form["gender"]
        qualification = request.form["qualification"]
        extraqualifi = request.form["extraqualifi"]
        sql = "update users set name=%s,phno=%s,address=%s,bday=%s,gender=%s,qualification=%s,extraqualifi=%s where id= %s"
        con.execute(
            sql, [name, phno, address, bday, gender, qualification, extraqualifi, id]
        )
        connection.commit()
        return redirect(url_for("home"))

@app.route("/deleteUser/<string:id>", methods=["GET", "POST"])
def deleteUser(id):
    con = connection.cursor()
    sql = "delete from users where id= %s"
    con.execute(sql, [id])
    connection.commit()
    con.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
