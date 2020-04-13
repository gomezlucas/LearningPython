from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=1)


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
        flash("You have succesfully logged In")
        return redirect(url_for("user"))


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html")
    else:
        flas("you are not logged In")
        return redirect(html_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
