from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.decks_model import Deck
from flask_app.models.all_cards_model import AllCard
from flask_app.models.cards_model import Card


# CRUD #TODO ASSIGN TABEL NAME IN FUNCTION NAMES AND URLS
@app.route("/all/user/<int:id>/decks")
def deck_get_all(id):
    data = {
        'user_id': id
    }
    all_decks = Deck.get_user_decks(data)
    return render_template("owned_decks.html", all_decks=all_decks)


@app.route("/deck/new")
def deck_new():
    if session.get("user_id") is None:
        return redirect("/")
    return render_template("new_deck.html")


@app.post("/deck/create")
def deck_create():
    if session.get("user_id") is None:
        return redirect("/")
    print("REQUEST.FORM-------------->", request.form)
    is_valid = Deck.validate_stuff(request.form)
    if is_valid:
        data = {
            **request.form,
            "user_id": session["user_id"],
        }
        new_deck = Deck.create(data)
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")


@app.route("/deck/<int:id>")
def deck_one(id):
    if session.get("user_id") is None:
        return redirect("/")
    data = {
        "id": id,
    }
    info = AllCard.get_cards(data)
    deck = Deck.get_one_join(data)
    type_checking = {
        "Creature": False,
        "creature_count": 0,
        "Sorcery": False,
        "sorcery_count": 0,
        "Instant": False,
        "instant_count": 0,
        "Artifact": False,
        "artifact_count": 0,
        "Enchantment": False,
        "enchantment_count": 0,
        "Land": False,
        "land_count": 0,
    }
    for stuff in info:
        if stuff["types"] == "Creature":
            type_checking["Creature"] = True
            type_checking["creature_count"] = type_checking["creature_count"] + 1

        elif stuff["types"] == "Sorcery":
            type_checking["Sorcery"] = True
            type_checking["sorcery_count"] = type_checking["sorcery_count"] + 1

        elif stuff["types"] == "Instant":
            type_checking["Instant"] = True
            type_checking["instant_count"] = type_checking["instant_count"] + 1

        elif stuff["types"] == "Artifact":
            type_checking["Artifact"] = True
            type_checking["artifact_count"] = type_checking["artifact_count"] + 1

        elif stuff["types"] == "Enchantment":
            type_checking["Enchantment"] = True
            type_checking["enchantment_count"] = type_checking["enchantment_count"] + 1

        elif stuff["types"] == "Land":
            type_checking["Land"] = True
            type_checking["land_count"] = type_checking["land_count"] + 1
    if info:
        info.sort(key=lambda x: x["cmc"])
    print(type_checking)
    return render_template(
        "view.html", deck=deck, info=info, type_checking=type_checking
    )  # TODO ASSIGN HTML FILE


@app.route("/deck/<int:id>/edit")
def deck_edit(id):
    if session.get("user_id") is None:
        return redirect("/")
    data = {"id": id}
    deck = Deck.get_one(data)
    cards = AllCard.get_all_join()
    for info in cards:
        print(info.id)
    info = AllCard.get_cards(data)
    type_checking = {
        "Creature": False,
        "creature_count": 0,
        "Sorcery": False,
        "sorcery_count": 0,
        "Instant": False,
        "instant_count": 0,
        "Artifact": False,
        "artifact_count": 0,
        "Enchantment": False,
        "enchantment_count": 0,
        "Land": False,
        "land_count": 0,
    }
    for stuff in info:
        if stuff["types"] == "Creature":
            type_checking["Creature"] = True
            type_checking["creature_count"] = type_checking["creature_count"] + 1

        elif stuff["types"] == "Sorcery":
            type_checking["Sorcery"] = True
            type_checking["sorcery_count"] = type_checking["sorcery_count"] + 1

        elif stuff["types"] == "Instant":
            type_checking["Instant"] = True
            type_checking["instant_count"] = type_checking["instant_count"] + 1

        elif stuff["types"] == "Artifact":
            type_checking["Artifact"] = True
            type_checking["artifact_count"] = type_checking["artifact_count"] + 1

        elif stuff["types"] == "Enchantment":
            type_checking["Enchantment"] = True
            type_checking["enchantment_count"] = type_checking["enchantment_count"] + 1

        elif stuff["types"] == "Land":
            type_checking["Land"] = True
            type_checking["land_count"] = type_checking["land_count"] + 1
    if info:
        info.sort(key=lambda x: x["cmc"])
    print("TYPE_CHECKING*********************************", type_checking)
    return render_template(
        "edit.html", deck=deck, info=info, type_checking=type_checking
    )  # TODO ASSIGN HTML FILE


@app.post("/deck/<int:id>/update")
def deck_update(id):
    if session.get("user_id") is None:
        return redirect("/")
    is_valid = Deck.validate_stuff(request.form)
    if is_valid:
        data = {**request.form, "id": id}
        nothing = Deck.update_one(data)
        return redirect("/dashboard")  # TODO ADD ROUTE FOR REDIRECT
    else:
        return redirect(f"/deck/{id}/edit")


@app.route("/deck/<int:id>/delete")
def delete_deck(id):
    if session.get("user_id") is None:
        return redirect("/")
    data = {"id": id}
    nothing = Deck.delete_cards_from_deck(data)
    nothing = Deck.delete_one(data)
    return redirect("/dashboard")  # TODO ADD ROUTE FOR REDIRECT
