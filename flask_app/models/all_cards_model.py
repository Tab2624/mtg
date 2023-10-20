from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
from flask_app.models import decks_model
import re


# model the class after the friend table from our database
class AllCard:  # TODO change class name// use pascel case
    def __init__(self, data: dict):
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # TODO Add additional columns from database here

    @classmethod
    def create(cls, data: dict):
        query = "INSERT INTO cards(name, colors, cmc, img_url, deck_id) VALUE ( %(name)s, %(colors)s, %(cmc)s, %(img_url)s, %(deck_id)s )"
        new_row_id = connectToMySQL(DATABASE).query_db(
            query, data
        )  # RETURNS back an INT, the ID of the row inserted
        return new_row_id

    @classmethod
    def get_all_join(cls):
        query = "SELECT * FROM cards join decks on decks.id = cards.deck_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        list_of_dict = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        cards = []  # TODO make changes to variable names

        if list_of_dict:
            for deck in list_of_dict:
                card = cls(deck)
                print("card---------------------->", card)
                data = {
                    **deck,
                    "id": deck["decks.id"],
                    "created_at": deck["decks.created_at"],
                    "updated_at": deck["decks.updated_at"],
                }
                deck_instance = decks_model.Deck(data)
                card.deck_instance = deck_instance
                cards.append(card)

        return cards

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cards WHERE id = %(id)s;"
        info = connectToMySQL(DATABASE).query_db(query, data)
        card_object = cls(info[0])
        # make deck object is good practice
        return card_object

    @classmethod
    def update_one(cls, data):
        query = "UPDATE cards SET name=%(name)s WHERE id = %(id)s;"  # TODO Name table, column, and value
        return connectToMySQL(DATABASE).query_db(query, data)  # RETURNS "none"

    @classmethod
    def delete_one(cls, id: dict):
        query = "DELETE FROM cards WHERE id = %(id)s;"  # TODO Name table
        return connectToMySQL(DATABASE).query_db(query, id)  # Returns "None"

    @staticmethod
    def validate_stuff(data: dict) -> bool:  # TODO change validator name accordingly
        is_valid = True
        print(data)
        # run through some if checks -> come to be bad, then is_valid = False
        # TODO add validations!
        if len(data["name"]) < 3:
            flash("Name too short", "err_cards_name")
            is_valid = False

        return is_valid

    @classmethod
    def get_one_join(cls, data):
        query = "SELECT * FROM cards join decks on decks.id = cards.deck_id WHERE cards.id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        list_of_dict = connectToMySQL(DATABASE).query_db(query, data)
        print("QUERY HERE------------------->", list_of_dict)
        # Create an empty list to append our instances of friends
        # TODO make changes to variable names

        if list_of_dict:
            card = cls(list_of_dict[0])  # equal to our query
            data = {
                **list_of_dict[0],
                "id": list_of_dict[0]["decks.id"],
                "created_at": list_of_dict[0]["decks.created_at"],
                "updated_at": list_of_dict[0]["decks.updated_at"],
            }
            deck_instance = decks_model.deck(data)
            card.deck_instance = deck_instance

        return card

    @classmethod
    def get_cards(cls, data):
        query = """
        SELECT *
        FROM cards
        INNER JOIN all_cards ON cards.all_card_id = all_cards.id
        WHERE cards.deck_id = %(id)s;
    """
        my_results = connectToMySQL(DATABASE).query_db(query, data)
        return my_results

    @staticmethod
    def card_validator(data):
        is_valid = True
        if len(data["name"]) < 0:
            flash("card name cannot be empty", "err_all_cards_name")
            is_valid = False
