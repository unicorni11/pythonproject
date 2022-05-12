from flask import Flask
from flask import render_template
from flask import request
import daten
import json
from datetime import datetime


app = Flask("__name__")


#Verlinkung auf Hauptseite
@app.route("/")
def start():
    name = "Anna-Lena"
    return render_template("index.html", name=name)

@app.route("/shop")
def schmuckshop():

    return render_template("shop.html")

@app.route("/formular", methods=['GET', 'POST']) #Verlinkung Formular
def formular():
    if request.method == 'POST':
        data = request.form
        name = data["name"]
        was = data.get("was")
        welche = data.get("welche")
        anzahl = data.get("anzahl")
        gravur = data["gravur"]
        zeitstempel = datetime.now()

        try:
            with open("bestellung.json", "r") as open_file:  # r für read = lesen
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Was": was, "Welche": welche, "Anzahl": anzahl, "Gravur": gravur, "Zeitstempel": zeitstempel}
        datei_inhalt.append(my_dict)

        with open("bestellung.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4, default=str)  # indent=4 das es schöne aussieht
        return str("Danke für deine Eingabe, die Daten wurden gespeichert.")
    else:
        return render_template("formular.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)




