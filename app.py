from flask import Flask, redirect, render_template, session, request
from extraUsage import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key" #change key when the application is deployed


db = sqlite3.connect("realtor.db")
cur = db.cursor()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            print("ERROR")

        # Ensure password was submitted
        elif not request.form.get("password"):
            print("ERROR")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            print("ERROR")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("auth/login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""
    if request.method == "POST":
        #get info from html
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not name:
            print("ERROR")

        # Ensure password was submitted
        elif not password:
            print("ERROR")

        #verify if password match with confirm your password
        elif password != confirmation:
            print("ERROR")


        #Get username to check for duplicates
        checkUsername = db.execute("SELECT * FROM users WHERE username = ?", name)

        if checkUsername:
            print("ERROR")

        else:
            #Add hash to the password
            newPassword = generate_password_hash(password, method='pbkdf2', salt_length=16)

            #Add username and password to database
            rowInsert = db.execute(
                "INSERT INTO users (username, hash) VALUES(?,?)", name, newPassword
            )
            # Remember which user has logged in
            #session["user_id"] = rowInsert[0]["id"]

            return redirect("/")

    else:
        return render_template("auth/register.html")
    
    
@app.route("/buyers")
def buyers():
    return render_template("buyers.html")

@app.route("/sellers")
def sellers():
    return render_template("sellers.html")

@app.route("/realtors")
def realtors():
    return render_template("realtors.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route("/termConditions")
def termConditions():
    return render_template("termConditions.html")

@app.route("/privacyPolicy")
def privacyPolicy():
    return render_template("privacyPolicy.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")