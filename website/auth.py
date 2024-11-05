from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re

from . import models
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
            else:
                # don't let the user know between account not existing and wrong email/password
                flash("Wrong email / password", category="error")
        else:
            # don't let the user know between account not existing and wrong email/password
            flash("Wrong email / password", category="error")
        pass
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        user = models.User.query.filter_by(email=email).first()

        if user:
            flash(
                "It seems you already created an account. Try with another email.",
                category="error",
            )
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            flash("Invalid email", category="error")
        elif len(name) < 3:
            flash("Name should be at least 4 characters", category="error")
        elif len(password) < 7:
            flash("Password should be at least 8 characters", category="error")
        elif password != cpassword:
            flash("Password doesn't match", category="error")
        else:
            new_user = models.User(
                email=email,
                full_name=name,
                password=generate_password_hash(password, method="pbkdf2:sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html")
