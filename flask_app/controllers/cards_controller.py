from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.cards_model import (
    Card,
)  # TODO change "model" to model name, and friend to class name
from flask_app.models.all_cards_model import (
    AllCard,
)  # TODO change "model" to model name, and friend to class name

# from flask_app.models.model_name import Classname #TODO add class name, add model name


@app.route("/card/new")
def card_new():
    if session.get("user_id") is None:
        return redirect("/")
    return render_template("new_card.html")


@app.post("/card/create")
def card_create():
    if session.get("user_id") is None:
        return redirect("/")
    is_valid = AllCard.card_validator(request.form)
    if is_valid:
        data = {
            **request.form,
            "user_id": session["user_id"],
        }
        new_card = Card.create(data)
        return redirect("/dashboard")  # redirect #TODO ADD ROUTE FOR REDIRECT
    else:
        return redirect("/card/new")


@app.route("/card/<int:id>/delete")
def delete_card(id):
    if session.get("user_id") is None:
        return redirect("/")
    data = {"id": id}
    to_delete = Card.delete_one(data)
    return redirect(f'/deck/{session["deck_id"]}/edit')  # TODO ADD ROUTE FOR REDIRECT


@app.post("/addcard/<int:id>/update")
def add_card(id):
    if session.get("user_id") is None:
        return redirect("/")
    session["deck_id"] = id
    data = {**request.form, "deck_id": session["deck_id"]}
    is_valid = Card.validate_stuff(data)
    if is_valid:
        nothing = Card.add_card(data)
        return redirect(f"/deck/{id}/edit")
    else:
        return redirect(f"/deck/{id}/edit")
