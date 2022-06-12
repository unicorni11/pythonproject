from flask import Flask
from flask import render_template
from flask import request, redirect
import json
from datetime import datetime
import plotly.express as px
from plotly.offline import plot

#Name App
app = Flask("__name__")


#Verlinkung auf Hauptseite
@app.route("/") #URL einen Pfad zuweisen (dynamisch)
def start(): #defintion der Funktion, welche Ausgeführt werden soll
    name = "Anna-Lena" #name der Ausgeben wird
    return render_template("index.html", name=name) #Rückgabe der Funktion

#
@app.route("/formular", methods=['GET', 'POST']) #Verlinkung Formular, Get: Daten vom Server anfordern (Bestimmte Ressoruce wird zurückgesendet), Post: verarbeitete Daten weitergesendet (Mit Server sprechen)
def formular():
    daten_uebermittelt = False #Boolsche Operation (Aussagen auf Richtigkeit prüfen) #0
    if request.method == 'POST': #Html zur weiterverarbeitung wird weitergesendet,
        data = request.form #Daten in Liste
        name = data["name"] #Listenelement Eingeben in ein textfeld
        adresse = data["adresse"]
        was = data.get("was") #Tuple Unveränderbare Liste , Dropdown Menü
        welches = data.get("welches")
        anzahl = data.get("anzahl")
        gravur = data["gravur"]
        zeitstempel = datetime.now() #Datum & Uhrzeit werden generiert

        daten_uebermittelt = True; #1

        if was == "Kette": # Trifft zustand zu oder nicht?
            preis = 3000 * int(anzahl) #preisfunktion, int: Ganzzahlige Werte
        elif was == "Armband": #Wenn if nicht erfüllt elif ausführen
                    preis = 1500 * int(anzahl)
        elif was == "Ring":
                    preis = 1000 * int(anzahl)
        elif was == "Ohrring":
                    preis = 2500 * int(anzahl)

        try: #auf error des codes testen
            with open("bestellung.json", "r") as open_file:  # r für read = lesen
                datei_inhalt = json.load(open_file) # liste in die json datei laden
        except FileNotFoundError: #falls error, leere Liste
            datei_inhalt = [] #leere Liste

        #dict erstellen mit value & key
        my_dict = {"Name": name, "Adresse": adresse, "Was": was, "Welches": welches, "Anzahl": anzahl, "Gravur": gravur, "Zeitstempel": zeitstempel, "Bestellstatus": "", "Preis": preis}
        datei_inhalt.append(my_dict) #Wert einer Liste hinzufügen

        with open("bestellung.json", "w") as open_file: # w= write
            json.dump(datei_inhalt, open_file, indent=4, default=str) #dumpp=konvertiert ein Python-Objekt in einen JSON-String. indent=4 das es schöne aussieht, default=standardwert str= Zahlen als Text
        return render_template("formular.html", daten_uebermittelt=daten_uebermittelt) #liste auflisten mit Jinja Logic,
    else:
        return render_template("formular.html") #Wenn Url nicht mit Post methode aufgerufen, dann über bestellungen.html gerendert werden


@app.route("/bestellungen")
def bestellungen():
    bestell_uebersicht = [] #leere Liste

    try: #auf error des codes testen
        with open("bestellung.json", "r") as open_file:  # r für read = lesen
            datei_inhalt = json.load(open_file) #liste in json datei laden
    except FileNotFoundError:
        datei_inhalt = [] #leere liste ausgeben

    for element in datei_inhalt:
        if element["Gravur"] == "": #falls keine Eingabe getätigt wird
            gravurwert = "keine Gravur"
        else:
            gravurwert = element["Gravur"]

        bestell_uebersicht.append([element["Name"], element["Adresse"], element["Was"], element["Welches"], element["Anzahl"], gravurwert]) #[] Listensymbol
        # Werte einer Liste hinzufügen

    return render_template("bestellungen.html", bestell_uebersicht=bestell_uebersicht) #Wert einer Liste hinzufügen


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
    app.run(debug=True, port=5000) #Debugging (Behebung von Fehlern) wird eingeschalten, App lauft über Rechner Port 5000




