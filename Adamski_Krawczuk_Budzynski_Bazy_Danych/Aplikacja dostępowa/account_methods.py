import gc
from flask import Flask, render_template, session, flash, redirect, url_for, request
from passlib.handlers.sha2_crypt import sha256_crypt

from decorators import login_required, logout_required


from dbconnect import connection


# app = Flask(__name__)


@login_required
@app.route('/logged/')
def alredy_logged_in():
    return render_template("you_are_already_logged_in.html")



@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))



@app.route('/login/', methods=["GET", "POST"])
@logout_required
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = '%s' " % (request.form["username"]))

            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("homepage"))

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        error = "Exception"
        return render_template("login.html", error=error)

