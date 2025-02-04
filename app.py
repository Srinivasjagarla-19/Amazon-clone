from flask import Flask, render_template as r, session, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)


app.secret_key = "d4b9"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "amazon"

mysql = MySQL(app)

@app.route("/")
def Amazonstru():
    return r("Amazonstru.html")

@app.route("/sign", methods=["POST", "GET"])
def sign():
    if request.method == "POST" and "email" in request.form and "pass" in request.form:
        email = request.form["email"]
        password = request.form["pass"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM client WHERE email=%s and password=%s", (email, password))
        user = cur.fetchone()
        if user:
            session["LoggedIn"] = True
            session["name"] = user["name"]
            session["Password"] = user["password"]
            session["Email"] = user["email"]
            return r("profile.html")
        else:
            return r("sign.html")
    return r("sign.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST" and 'name' in request.form and 'pass' in request.form and 'email' in request.form:
        name = request.form["name"]
        password = request.form["pass"]
        email = request.form["email"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO client (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
        mysql.connection.commit()
        cur.close()
        return r('sign.html')
    else:
        return r("register.html")

@app.route("/profile")
def profile():
    return r("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
