# Projektidee

### 1. Ausgangslage des Projektes

   Unser Familienunternehmen Herzog & Loibner befindet sich im Herzen von Vaduz. Seit fünf
   Jahren hat das Unternehmen ihre eigene Schmuckmarke „Aldusblatt“. Es handelt sich hierbei um hochwertigen 18 Karat
   Schmuck. Um die Aldusblattkollektion weiter zu vermarken möchte das Unternehmen einen Onlineshop zur Verfügung
   stellen. Die Produkte können ausgewählt werden & mittels Versand an die jeweilige Adresse geliefert werden.

2. Projektidee 

Der Online Shop ist so aufgebaut, dass auf der Startseite die verschiedenen Produktmöglichkeiten mit
   Informationen aufgezeigt werden. Nun hat man die Möglichkeit ein Produkt auszuwählen und gelangt somit auf das
   Bestell Formular. Für eine neue Bestellung werden alle Felder von Name bis Anzahl vollständig ausgefüllt. Zusätzlich
   bietet der Shop auch eine kostenlose Gravur an. Falls keine Gravur gewünscht wird, wird dies in der Bestellübersicht
   unter „Keine Gravur“ angezeigt. Sind alle Daten erfasst, können diese in das Bestellformular übermittelt werden.
   Abgespeichert werden die Daten in einem Json-File.

Der Shop Moderator hat nun die Möglichkeit, intern die Bestellliste im Backend einzusehen. Das Backend zeigt auf welchen
Umsatz mit welchem Produkt generiert wurde. Da das bestellte Produkt an die angebende Adresse versendet wird, muss
zuerst geklärt werden, ob sich dieses Produkt im Lager befindet. Somit kann der Shop Moderator in der Bestellliste
folgende Funktionen auswählen: nicht im Lager, im Lager & versendet. Diese Daten werden gespeichert und in der
Bestellübersicht unter „…“ aufgezeigt. So wissen die Mitarbeiter, welche Produkt noch versendet werden müssen.

3. Ablaufdiagramm

Produktbestellung:

Backend Funktion:

4. Anleitung/Walkthrough

Installation & Benutzung

• Downloaden Sie das Verzeichnis "Projekt" (https://github.com/unicorni11/pythonproject.git)
• Starten Sie die Python-Datei "main.py" auf ihrem Rechner. • Öffnen Sie diesen Link via
Webbrowser: "http://127.0.0.1:5000"
• Im Verzeichnis wurden aktuell Beispieldaten abgelegt. Wenn sie möchten, können Sie die Daten im „bestellungen.json“
löschen. So bekommen Sie eine leere Webapplikation und Sie beginnen bei null. • Start: Wenn Sie die Webapplikation
öffnen müssen Sie zuerst eine Bestellung vornehmen um einen Bestelleintrag zu generieren.

Funktionsbeschreibung

Damit das Programm einwandfrei funktioniert, muss in der main-Datei neben Flask auch, Json, datetime und Plotly Express
installiert bzw. importiert werden.

from flask import Flask from flask import render_template from flask import request, redirect import json from datetime
import datetime import plotly.express as px from plotly.offline import plot

Startseite (index.html)
• Hier befindet sich der Produktkatalog zu Veranschaulichung der auszuwählenden Produkte mit Preis • Mit einem Klick auf
„Bestellen“ wird man auf das Bestellformular geführt

Daten der Bestellung erfassen (formular.html)
• Mit Hilfe von diesem Formular werden die notwendigen Daten über die Bestellung erfasst • Name: Name der Person (z.B.
Anna-Lena Loibner)
• Adresse: Adresse der Person (z.B. Riedstrasse 2)
• Produktauswahl: Produkt & Material des Produkt wird bestimmt • Anzahl: die gewünschte Anzahl des Produktes • Gravur:
Wer möchte, kann eine Gravur hinzufügen. Ansonsten bleibt das Feld leer und in der Bestellliste wird „keine Gravur“
angezeigt

Bestellübersicht (bestellungen.html)
• Zur Veranschaulichung der eingegangen Bestellungen

Backend (backend.html)
• Hier wird der Status der Bestellung erfasst und aufgelistet • Über das Statusformular „Auswahl“ kann zwischen: nicht
im Lager, im Lager und Versendet ausgewählt werden • Danach wird im Bereich „Status“ die aktuelle Situation der
Bestellung aufgelistet • Zudem zeigt das Backend eine Auslistung der einzelnen Umsätze der Produkte sowie der
Gesamtumsatz auf.

Bootstrap

Bootstrap ist ein kostenloses und quelloffenes Frontend-Web-Framework zur Erstellung von Webseiten. Es dient der
Visualisierung & schöneren Darstellung. Der Link wurde hierbei im header eingefügt.

5. FAQ's

