from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
from flask_app.models import users_model
import re


# model the class after the friend table from our database
class Deck:  # TODO change class name// use pascel case
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # TODO Add additional columns from database here

    @classmethod
    def create(cls, data: dict):
        query = "INSERT INTO decks(name, user_id) VALUE ( %(name)s, %(user_id)s )"
        new_row_id = connectToMySQL(DATABASE).query_db(
            query, data
        )  # RETURNS back an INT, the ID of the row inserted
        return new_row_id

    @classmethod
    def get_all_join(cls):
        query = "SELECT * FROM decks join users on users.id = decks.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        list_of_dict = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        decks = []  # TODO make changes to variable names

        if list_of_dict:
            for user in list_of_dict:
                deck = cls(user)
                print("deck---------------------->", deck)
                data = {
                    **user,
                    "id": user["users.id"],
                    "created_at": user["users.created_at"],
                    "updated_at": user["users.updated_at"],
                }
                user_instance = users_model.User(data)
                deck.user_instance = user_instance
                decks.append(deck)

        return decks

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM decks WHERE id = %(id)s;"
        info = connectToMySQL(DATABASE).query_db(query, data)
        if not info:
            return []
        deck_object = cls(info[0])
        # make user object is good practice
        return deck_object

    @classmethod
    def update_one(cls, data):
        query = "UPDATE decks SET name=%(name)s WHERE id = %(id)s;"  # TODO Name table, column, and value
        return connectToMySQL(DATABASE).query_db(query, data)  # RETURNS "none"

    @classmethod
    def delete_one(cls, data: dict):
        query = "DELETE FROM decks WHERE id = %(id)s;"  # TODO Name table
        return connectToMySQL(DATABASE).query_db(query, data)  # Returns "None"

    @classmethod
    def delete_cards_from_deck(cls, data: dict):
        query = "DELETE FROM cards WHERE deck_id = %(id)s;"  # TODO Name table
        return connectToMySQL(DATABASE).query_db(query, data)  # Returns "None"

    @staticmethod
    def validate_stuff(data: dict) -> bool:  # TODO change validator name accordingly
        is_valid = True
        # run through some if checks -> come to be bad, then is_valid = False
        # TODO add validations!
        if len(data["name"]) <= 3:
            flash("Name must be at least 4 characters", "err_decks_name")
            is_valid = False
        if len(data["name"]) <= 3:
            flash("Name must be at least 4 characters", "err_decks_new_name")
            is_valid = False

        return is_valid

    @classmethod
    def get_one_join(cls, data):
        query = "SELECT * FROM decks join users on users.id = decks.user_id WHERE decks.id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        list_of_dict = connectToMySQL(DATABASE).query_db(query, data)
        print("QUERY HERE------------------->", list_of_dict)
        # Create an empty list to append our instances of friends
        # TODO make changes to variable names

        if list_of_dict:
            deck = cls(list_of_dict[0])  # equal to our query
            print("deck---------------------->", deck)
            data = {
                **list_of_dict[0],
                "id": list_of_dict[0]["users.id"],
                "created_at": list_of_dict[0]["users.created_at"],
                "updated_at": list_of_dict[0]["users.updated_at"],
            }
            user_instance = users_model.User(data)
            deck.user_instance = user_instance

        return deck
