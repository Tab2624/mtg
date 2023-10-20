from flask import render_template, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app
from flask_app.models.decks_model import Deck
from mtgsdk import Card

# from flask_app.models.model_name import Classname #TODO add class name, add model name


@app.route("/")
def index():
    return render_template("landing_page.html")


@app.route("/login/register")
def login_register():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if session.get("user_id") is None:
        return redirect("/")
    decks = Deck.get_all_join()
    decks.sort(key=lambda deck: deck.created_at, reverse=True)
    return render_template("dashboard.html", decks=decks)


@app.route("/fill/db")
def fill_db():
    if session.get("user_id") is None:
        return redirect("/")
    all_cards = []
    cards = Card.all()

    for card in cards:
        if card.image_url is not None and card.name not in all_cards:
            another_list = [
                card.name,
                card.colors,
                card.cmc,
                card.types,
                card.image_url,
            ]
            all_cards.append(another_list)

    # Initialize an empty list to store the data to be inserted into the database
    data_to_insert = []

    for card in all_cards:
        if card[1] is None:
            card[1] = ["None"]
        if card[3] == "" or card[3] is None:
            pass

        name = card[0]
        color = card[1][0]
        cmc = card[2]
        types = card[3][0]
        img_url = card[4]

        # Append the data to the list for batch insertion
        data_to_insert.append((name, color, cmc, types, img_url))
    print("DATA TO INSERT----------->", data_to_insert)

    # Define the SQL query with placeholders
    query = "INSERT INTO all_cards (name, colors, cmc, types, img_url) VALUES (%s, %s, %s, %s, %s)"

    # Insert all the data into the database in a single transaction
    mysql = connectToMySQL(DATABASE)
    cursor = mysql.connection.cursor()

    try:
        print("BEFORE CURSOR.EXECUTEMANY---------------------->")
        cursor.executemany(query, data_to_insert)
        print("AFTER CURSOR.EXECUTEMANY------------->")
        mysql.connection.commit()
        print("CHANGES SHOULD'VE BEEN MADE")
    except Exception as e:
        print("EXCEPTION ERROR HERE--------------------->", e)
        mysql.connection.rollback()
        # Handle the exception or log the error here

    cursor.close()
    return redirect("/dashboard")
