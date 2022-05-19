from flask import Flask
from flask import render_template
from flask import request
import json
from datetime import datetime


app = Flask("__name__")


#Verlinkung auf Hauptseite
@app.route("/")
def start():
    name = "Anna-Lena"
    return render_template("index.html", name=name)


@app.route("/formular", methods=['GET', 'POST']) #Verlinkung Formular
def formular():
    daten_uebermittelt = False
    if request.method == 'POST':
        data = request.form
        name = data["name"]
        adresse = data["adresse"]
        was = data.get("was")
        welches = data.get("welches")
        anzahl = data.get("anzahl")
        gravur = data["gravur"]
        zeitstempel = datetime.now()

        daten_uebermittelt = True;

        try:
            with open("bestellung.json", "r") as open_file:  # r für read = lesen
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Name": name, "Adresse": adresse, "Was": was, "Welches": welches, "Anzahl": anzahl, "Gravur": gravur, "Zeitstempel": zeitstempel}
        datei_inhalt.append(my_dict)

        with open("bestellung.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4, default=str)  # indent=4 das es schöne aussieht
        return render_template("formular.html", daten_uebermittelt=daten_uebermittelt)
    else:
        return render_template("formular.html")


@app.route("/bestellungen")
def bestellungen():
    bestell_uebersicht = []

    try:
        with open("bestellung.json", "r") as open_file:  # r für read = lesen
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    for element in datei_inhalt:
        if element["Gravur"] == "":
            gravurwert = "keine Gravur"
        else:
            gravurwert = element["Gravur"]

        bestell_uebersicht.append([element["Name"], element["Adresse"], element["Was"], element["Welches"], element["Anzahl"], gravurwert])


    return render_template("bestellungen.html", bestell_uebersicht=bestell_uebersicht)


@app.route("/backend", methods=["GET", "POST"])
def backend():
    bestell_uebersicht = []

    try:
        with open("bestellung.json", "r") as open_file:  # r für read = lesen
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    for element in datei_inhalt:
        if element["Gravur"] == "":
            gravurwert = "keine Gravur"
        else:
            gravurwert = element["Gravur"]

        bestell_uebersicht.append(
            [element["Name"], element["Adresse"], element["Was"], element["Welches"], element["Anzahl"], gravurwert, element["Zeitstempel"]])

    if request.form.get("zeitstempel") == element["Zeitstempel"]:
        print("test1234")
        for element in datei_inhalt:
            if request.form.get("zeitstempel") == element["Zeitstempel"]:
                print(element["Name"])


    return render_template("backend.html", bestell_uebersicht=bestell_uebersicht)


@app.route("/visualisierung")
def visualisierung():

    return render_template("visualisierung.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)




