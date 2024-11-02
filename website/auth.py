from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    pass
    
  return render_template("login.html", text="Loading...")

@auth.route('/logout')
def logout():
  return "<p>Logout</p>"

@auth.route('/signup', methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    cpassword = request.form.get("cpassword")
    
    if password != cpassword:
      flash("Password doesn't match", category="error")
    else:
      flash("Account created!", category="success")  
    
    
  
  return render_template("signup.html")