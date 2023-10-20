from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.users_model import User

bcrypt = Bcrypt(app)


@app.post("/register/user")
def register():
    is_valid = User.validate_register(request.form)
    # Call the save @classmethod on User
    # store user id into session
    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        print(pw_hash)
        # put the pw_hash into the data dictionary
        data = {
            "first_name": request.form[
                "first_name"
            ],  # TODO add all columns from users table
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash,
        }
        user_id = User.save(data)
        session["user_id"] = user_id
        session["first_name"] = request.form["first_name"]
        print("SESSION REGISTER--------------------->", session)
        return redirect("/dashboard")
    else:
        return redirect("/login/register")


@app.post("/logout")
def logout():
    del session["first_name"]
    del session["user_id"]
    return redirect("/")


@app.route('/user/login')
def user_login():
    return render_template('login.html')


@app.post("/login")
def login():
    is_valid = User.validate_login(request.form)
    if is_valid:
    # see if the username provided exists in the database
        data = {"email": request.form["email"]}
        user_in_db = User.get_by_email(data)
    # user is not registered in the db
        if not user_in_db:
            flash("Invalid Email/Password", "err_login_info")
            return redirect("/user/login")
        if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        # if we get False after checking the password
            flash("Invalid Email/Password", "err_login_info")
            return redirect("/")
    # if the passwords matched, we set the user_id into session
        session["first_name"] = user_in_db.first_name
        session["user_id"] = user_in_db.id
        print("SESSION LOGIN---------------->", session)
    # never render on a post!!!
        return redirect("/dashboard")
    else: return redirect('/user/login')
