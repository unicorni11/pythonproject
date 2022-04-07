from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import random
from datetime import datetime

from rechnen.steuernn import berechnen
from rechnen.steuernn import abgaben

app = Flask("__name__")


@app.route("/")
def hello():
    names = ["Anna", "Eileen", "Selina", "Rebekka", "Bianca"]
    name_choice = random.choice(names)
    about_link = url_for("about")
    return render_template("index.html", name=name_choice, link=about_link)


@app.route("/about")
def about():
    return "text about"


@app.route("/hello/names")
def begruessung(names):
    return "Hallo " + names + "!"


@app.route("/form", methods=["get", "post"])
def form():
    if request.method.lower() == "get":
        return render_template("formular.html")
    if request.method.lower() == "post":
        name = request.form["vorname"]
        return name


@app.route("/liste")
def auflistung():
    elemente = ["Bla", "Blubber", "Käsekuchen"]
    return render_template("liste.html", html_elemente=elemente)


@app.route("/table")
def tabelle():
    biere = [
        {
            "name": "Glatsch",
            "herkunft": "Chur",
            "vol": "4.0",
            "brauerei": "Calanda",
            "preis": 3.5
        },
        {
            "name": "Retro",
            "herkunft": "Luzern",
            "vol": "4.9",
            "brauerei": "Eichhof",
            "preis": 3.0
        },
        {
            "name": "Quellfrisch",
            "herkunft": "Appenzell",
            "vol": "4.8",
            "brauerei": "Locher",
            "preis": 2.0
        },
             ]
    for bier in biere:
        preis = bier["preis"]
        tax = berechnen(preis)
        bier["steuern"] = tax

    table_header = ["Name", "Herkunft", "Vol", "Brauerei", "Preis"]
    return render_template("beer.html", beers=biere, header=table_header)


@app.route("/demo_chf", methods=["get", "post"])
def egal_was():
    if request.method.lower() == "get":
        return render_template("preis.html")
    if request.method.lower() == "post":
        preis = request.form["preis"]
        preis = float(preis)
        abgaben_betrag = abgaben(preis)
        now = datetime.now()
        with open("jail_free_card.txt", "a", encoding="utf8") as offene_datei:
            offene_datei.write(f"{now},{preis},{abgaben_betrag}\n")
        return render_template("preis.html", abgabe=abgaben_betrag)


@app.route("/demo_euro")
def egal_was_2():
    abgaben_betrag = abgaben(400)
    return f"{abgaben_betrag} Euro"


@app.route("/datum")
def datum_anzeigen():
    with open("jail_free_card.txt", encoding="utf8") as open_file:
        inhalt = open_file.read()
    return inhalt.replace("\n", "<br>")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
