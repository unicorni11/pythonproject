import plotly.express as px
from plotly.offline import plot
import main

def bestellung():
    eingabe = main.bestellungen() #daten von bestellung.json werden aufgerufen
    produkt = []
    produktanzahl = []

    #ergänzt die leeren Listen dauer und sportart mit den Eingabedaten aus data.json
    for key, value in eingabe.items():
        was = value["Was"]uz
        anzahl = value["Anzahl"]
        produkt.append(duration)
        produktanzahl.append(sport)

    return produkt, produktanzahl

#pie-chart von Plotly https://plotly.com/python/pie-charts mit den Daten aus der Funktion data()
#in den code-snippets von Plotly wird fig.show() verwendet. fig.show() öffnet ein eigenes Browserfenster. Daher div, um Diagramm im Sports Tracker anzeigen zu können
def viz():
    produkt, produktanzahl = bestellung()
    fig = px.pie(values=was, names=anzahl,
                 labels={"values": "Was", "names": "Anzahl},
                 title="Erfasste Bestellunngen dargestellt nach Produktart und Anzahl an Verkauften Waren")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    div = plot(fig, output_type="div")
    return div