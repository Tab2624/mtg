from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
import re

PASSWORD_REGEX = re.compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_register(data: dict) -> bool:
        is_valid = True
        print("HELLO FROM VALIDATOR-------------------->")
        print(data)
        # run through some if checks -> come to be bad, then is_valid = False
        # TODO add validations!
        if len(data["first_name"]) < 2:
            flash("First name too short", "err_users_first_name")
            is_valid = (
                False  # Remember, do not return False, but return the variable False!
            )

        if len(data["last_name"]) < 2:
            flash("Last name too short", "err_users_last_name")
            is_valid = (
                False  # Remember, do not return False, but return the variable False!
            )

        if len(data["email"]) < 2:
            flash("Email too short", "err_users_email")
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "err_users_email")
            is_valid = (
                False  # Remember, do not return False, but return the variable False!
            )

        if len(data["password"]) < 2:
            flash("Password too short", "err_users_password")
            is_valid = (
                False  # Remember, do not return False, but return the variable False!
            )
        elif not PASSWORD_REGEX.match(data["password"]):
            flash(
                "Password must contain eight characters, one uppercase and lowercase required",
                "err_users_password",
            )
            is_valid = (
                False  # Remember, do not return False, but return the variable False!
            )

        if not data["password"] == data["confirm_password"]:
            flash("Passwords do not match", "err_users_confirm_password")
            is_valid = False
        # At the end

        if is_valid:
            print("second is valid check")
            potential_user = User.get_one_by_email(data)
            # if potential_user is "TRUE"--> it already exists
            if potential_user:
                print("inside the if")
                flash("email address already in use", "err_users_email")
                is_valid = False

        return is_valid

    @classmethod
    def get_one_by_email(cls, data: dict):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []

        dict = results[0]
        instance = cls(dict)
        return instance

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
