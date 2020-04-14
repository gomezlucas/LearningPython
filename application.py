from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qtkcvpmkvldwfy:7b437f1ac7cb1468ce4273af05b9a2ce8276d3b82a584eab157e6e51b4aa9e1a@ec2-3-91-112-166.compute-1.amazonaws.com:5432/d8ufsgg72h6v8h"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=1)


db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email =  email



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user" in session:
            flash("You have already logged In")
            return redirect(url_for("user"))
        else:
            return render_template("login.html")
    else:
        session.permanent = True
        user = request.form["user"]
        session["user"] = user
        query = users.query.filter_by(name=user).first()
        if query:
            session[email] = found_user.email
        else:
            usr = users(user,None)
            db.session.add(usr)
            db.session.commit()
        
        
        flash("You have succesfully logged In")
        return redirect(url_for("user"))


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            query = users.query.filter_by(name=user).first()
            query.email = email
            db.session.commit()

            flash("email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("you are not logged In")
        return redirect(url_for("login"))


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
