from flask import Flask
from flask import render_template
from flask import request, redirect
import json
from datetime import datetime
import plotly.express as px
from plotly.offline import plot

# Name App
app = Flask("__name__")


# Verlinkung auf Hauptseite, Python Funktion in Flask umwandeln
@app.route("/")  # URL einen Pfad zuweisen (dynamisch)
def start():  # definition der Funktion, welche Ausgeführt werden soll
    name = "Anna-Lena"  # name der Ausgegeben wird
    return render_template("index.html", name=name)  # Rückgabe der Funktion, durch Grafik


# Verlinkung auf Formularseite
@app.route("/formular", methods=["GET", "POST"])  # Get: Daten vom Server anfordern (Bestimmte Ressoruce wird zurückgesendet)
def formular():  # Post: verarbeitete Daten weitergesendet (Mit Server sprechen)
    if request.method == 'POST':  # Zustand trifft ein oder nicht?
        data = request.form  # Daten in Liste
        name = data["name"]  # Liste, Eingabe Name
        adresse = data["adresse"]
        was = data.get("was")  # get = Ausgabe des Wertes, mit ausgewähltem Schlüssel, Tupel= unveränderbare Listen
        welches = data.get("welches")
        anzahl = data.get("anzahl")
        gravur = data["gravur"]
        zeitstempel = datetime.now()  # Datum & Uhrzeit werden generiert

        daten_uebermittelt = True  # True (1): Dieser Ausdruck ist immer wahr

        if was == "Kette":  # Wenn Kette ausgewählt dann Rechne...
            preis = 3000 * int(anzahl)  # preisfunktion, int: Ganzzahlige Werte
        elif was == "Armband":  # Wenn Kette nicht ausgewählt dann elif ausführen
            preis = 1500 * int(anzahl)
        elif was == "Ring":
            preis = 1000 * int(anzahl)
        elif was == "Ohrring":
            preis = 2500 * int(anzahl)

        try:  # Ausnahmen behandeln, auf einen error den code testen
            with open("bestellung.json", "r") as open_file:  # r für read = lesen
                datei_inhalt = json.load(open_file)  # liste in die json datei laden
        except FileNotFoundError:  # falls error, als leere Liste anzeigen
            datei_inhalt = []  # leere Liste

        # dict erstellen für die Bestellübersicht, jedem Schlüssel wird ein Wert zugewiesen
        my_dict = {"Name": name, "Adresse": adresse, "Was": was, "Welches": welches, "Anzahl": anzahl, "Gravur": gravur,
                   "Zeitstempel": zeitstempel, "Bestellstatus": "", "Preis": preis}
        datei_inhalt.append(
            my_dict)  # Jedes Schlüssel-Wert-Paar in eine Liste hinzufügen, append: ende der Liste hinzufügen

        with open("bestellung.json", "w") as open_file:  # w= write
            json.dump(datei_inhalt, open_file, indent=4,
                      default=str)  # dumpp=konvertiert ein Python-Objekt in einen JSON-String. indent=4 das es schöne aussieht, default=standardwert str= Zahlen als Text
        return render_template("formular.html",
                               daten_uebermittelt=daten_uebermittelt)  # Rückgabe der Funktion, durch Grafik
    else:
        return render_template(
            "formular.html")  # Wenn Url nicht mit Post methode aufgerufen, dann über bestellungen.html gerendert werden


@app.route("/bestellungen")
def bestellungen():
    bestell_uebersicht = []

    try:
        with open("bestellung.json", "r") as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    for element in datei_inhalt:  # nächst kleinere Aufteilungsmöglichkeit
        if element["Gravur"] == "":  # nichts reingeschrieben
            gravurwert = "keine Gravur"
        else:
            gravurwert = element["Gravur"]

        bestell_uebersicht.append(
            [element["Name"], element["Adresse"], element["Was"], element["Welches"], element["Anzahl"], gravurwert])
        # Anzahl elemente die im Html definiert wurden, 0-5, [] Listenklammern

    return render_template("bestellungen.html", bestell_uebersicht=bestell_uebersicht)  # Rückgabe der Funktion


@app.route("/backend", methods=["GET", "POST"])
def backend():
    bestell_uebersicht = []

    try:
        with open("bestellung.json", "r") as open_file:  # r für read = lesen
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    # wie oben
    for element in datei_inhalt:
        if element["Gravur"] == "":
            gravurwert = "keine Gravur"
        else:
            gravurwert = element["Gravur"]

        bestell_uebersicht.append(
            [element["Name"], element["Adresse"], element["Was"], element["Welches"], element["Anzahl"], gravurwert,
             element["Zeitstempel"], element["Bestellstatus"]])
        # Anzahl elemente die im Html definiert wurden, 0-7, [] Listenklammern

    if request.method == "POST":  # Zustand trifft ein oder nicht?
        print("posttest")  # test ob server anfrage aufnimmt
        for element in datei_inhalt:  # Auswahl Buttons, mit Zeitstempel in Kombination
            if request.form.get(element[
                                    "Zeitstempel"]) == "nicht im Lager":  # wenn Ausgewählt nicht im Lager, status soll auf nicht im Lager gesetzt werden
                element["Bestellstatus"] = "nicht im Lager"
            elif request.form.get(element["Zeitstempel"]) == "im Lager":
                element["Bestellstatus"] = "im Lager"
            elif request.form.get(element["Zeitstempel"]) == "Versendet":
                element["Bestellstatus"] = "Versendet"

        with open("bestellung.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4,
                      default=str)  # dumpp=konvertiert ein Python-Objekt in einen JSON-String. indent=4 das es schöne aussieht, default=standardwert str= Zahlen als Text

        return redirect("backend")  # Rückgabe Backend Formular

    return render_template("backend.html",
                           bestell_uebersicht=bestell_uebersicht)  # Rückgabe der Bestellübersicht & jeweiligen Umsätze


@app.route("/visualisierung")
def datenvisualierung():
    bestell_uebersicht = []
    umsatz_gesamt = 0  # beginnt beim Umsatz 0
    umsatz_ketten = 0
    umsatz_armband = 0
    umsatz_ring = 0
    umsatz_ohrring = 0

    try:
        with open("bestellung.json", "r") as open_file:  # r für read = lesen
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    # Umsatzberechnung im Backend
    for element in datei_inhalt:
        umsatz_gesamt = umsatz_gesamt + element["Preis"]  # gesamtumsatz
        if element["Was"] == "Kette":
            umsatz_ketten = umsatz_ketten + element["Preis"]
        elif element["Was"] == "Armband":
            umsatz_armband = umsatz_armband + element["Preis"]
        elif element["Was"] == "Ring":
            umsatz_ring = umsatz_ring + element["Preis"]
        else:
            umsatz_ohrring = umsatz_ohrring + element["Preis"]

    balkendiagramm = px.bar(  # Balkendiagramm mit plotly
        x=["Kette", "Armband", "Ring", "Ohrring"],  # Daten für x-Achse des Diagramms
        y=[umsatz_ketten, umsatz_armband, umsatz_ring, umsatz_ohrring],  # Daten für y-Achse des Diagramms
        labels={"x": "Produktbeschreibung", "y": "Umsätze in CHF"}  # Achsenbeschriftung
    )
    div_balkendiagramm = plot(balkendiagramm, output_type="div")  # Balkendiagramm für Vergleich Höhenmeter


    return render_template("visualisierung.html", balkendiagramm=div_balkendiagramm, bestell_uebersicht=bestell_uebersicht, umsatz_gesamt=umsatz_gesamt,
                           umsatz_ketten=umsatz_ketten, umsatz_armband=umsatz_armband,
                           umsatz_ring=umsatz_ring,
                           umsatz_ohrring=umsatz_ohrring)  # Rückgabe der Bestellübersicht & jeweiligen Umsätze


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # Flask App soll mit folgenden Parametern starten
    # Debugging (Behebung von Fehlern) wird eingeschalten, App lauft über Rechner Port 5000
