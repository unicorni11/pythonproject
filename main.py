from flask import Flask
from flask import render_template
from flask import request, redirect
import json
from datetime import datetime
import plotly.express as px
from plotly.offline import plot


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

        if was == "Kette":
            preis = 3000 * int(anzahl)
        elif was == "Armband":
                    preis = 1500 * int(anzahl)
        elif was == "Ring":
                    preis = 1000 * int(anzahl)
        elif was == "Ohrring":
                    preis = 2500 * int(anzahl)

        try:
            with open("bestellung.json", "r") as open_file:  # r für read = lesen
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Name": name, "Adresse": adresse, "Was": was, "Welches": welches, "Anzahl": anzahl, "Gravur": gravur, "Zeitstempel": zeitstempel, "Bestellstatus": "", "Preis": preis}
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
    umsatz_gesamt = 0
    umsatz_ketten = 0
    umsatz_armband = 0
    umsatz_ring = 0
    umsatz_ohrring = 0

    try:
        with open("bestellung.json", "r") as open_file:  # r für read = lesen
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    #Berechnung Umsatz
    for element in datei_inhalt:
        umsatz_gesamt = umsatz_gesamt + element["Preis"]
        if element["Was"] == "Kette":
            umsatz_ketten = umsatz_ketten + element["Preis"]
        elif element["Was"] == "Armband":
            umsatz_armband = umsatz_armband + element["Preis"]
        elif element["Was"] == "Ring":
            umsatz_ring = umsatz_ring + element["Preis"]
        else:
            umsatz_ohrring = umsatz_ohrring + element["Preis"]


    for element in datei_inhalt:
        if element["Gravur"] == "":
            gravurwert = "keine Gravur"
        else:
            gravurwert = element["Gravur"]

        bestell_uebersicht.append(
            [element["Name"], element["Adresse"], element["Was"], element["Welches"], element["Anzahl"], gravurwert, element["Zeitstempel"], element["Bestellstatus"]])
    if request.method == "POST":
        print("posttest")
        for element in datei_inhalt:
            if request.form.get(element["Zeitstempel"]) == "nicht im Lager":
                element["Bestellstatus"] = "nicht im Lager"
            elif request.form.get(element["Zeitstempel"]) == "im Lager":
                element["Bestellstatus"] = "im Lager"
            elif request.form.get(element["Zeitstempel"]) == "Versendet":
                element["Bestellstatus"] = "Versendet"

        with open("bestellung.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4, default=str)  # indent=4 das es schöne aussieht

        return redirect("backend")

    return render_template("backend.html", bestell_uebersicht=bestell_uebersicht, umsatz_gesamt=umsatz_gesamt, umsatz_ketten = umsatz_ketten, umsatz_armband = umsatz_armband,
                           umsatz_ring = umsatz_ring, umsatz_ohrring = umsatz_ohrring)

@app.route("/visualisierung")
def visualisierung():
    balkendiagramm = px.bar(
        x=["Kette", "Armband", "Ringe", "Ohrringe"],
        y=[umsatz_ketten, umsatz_armband, umsatz_ring, umsatz_ohrring],
        labels={"x": "Produkt", "y": "Umsatz"}
    )
    div_balkendiagramm = plot(balkendiagramm, output_type="div")

    return render_template("visualisierung.html", balkendiagramm = div_balkendiagramm, umsatz_ketten = umsatz_ketten, umsatz_armband = umsatz_armband,
                           umsatz_ring = umsatz_ring, umsatz_ohrring = umsatz_ohrring)





if __name__ == "__main__":
    app.run(debug=True, port=5000)




