import urllib.request
import json
import os
import re
import PyPDF2

# Liste der zu suchenden Begriffe
regex = r"(Hauptausschuss|Rechnungsprüfungsausschuss|Wahlausschuss|Wahlprüfungsausschuss|Ausschuss für Kinder, Jugendliche und Familien|Ausschuss für Schule und Weiterbildung|Betriebsausschuss der Abfallwirtschaftsbetriebe Münster (AWM)|Betriebsausschuss citeq|Betriebsausschuss Münster Marketing|Ausschuss für Gleichstellung|Ausschuss für Personal, Digitalisierung, Organisation, Sicherheit und Ordnung|Ausschuss für Soziales, Gesundheit, Verbraucherschutz und Arbeitsförderung|Ausschuss für Stadtplanung und Stadtentwicklung|Ausschuss für Umweltschutz, Klimaschutz und Bauwesen|Ausschuss für Verkehr und Mobilität|Ausschuss für Wohnen, Liegenschaften, Finanzen und Wirtschaft|Kulturausschuss|Sportausschuss)"

pages = 1#9#80
i = 1

# Ergebnisliste
results = []

while i <= pages:
    url = "https://oparl.stadt-muenster.de/bodies/0001/files?page=" + str(i)

    # Store the response of URL
    response = urllib.request.urlopen(url)

    # Storing the JSON response from URL in data
    data_json = json.loads(response.read())

    a = 1
    while a < 25: # 25 Files-Elemente pro Seite die durchgelaufen werden müssen
        if data_json["data"][a]["name"] == "Berichtsvorlage" or data_json["data"][a]["name"] == "Beschlussvorlage":
            data = data_json["data"][a]["downloadUrl"]
            filename = os.path.basename(data)

            # Setzen Sie den Pfad, unter dem die PDF-Datei gespeichert werden soll

            file_path = "C:/Users/pvkip/OneDrive/Desktop/Oparl/" + filename.replace(".html", ".pdf")
            #Anpassungen vornehmen! Dokument soll mit Titel abgespeichert werden

            # Herunterladen der PDF-Datei
            with urllib.request.urlopen(data) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())

            # Öffnen der PDF-Datei
            with open(file_path, 'rb') as pdf_file:
                # Erstellen einer Instanz von PdfReader
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Durchsuchen des Dokuments nach Begriffen
                search_text = ""
                for page in pdf_reader.pages:
                    search_text += page.extract_text()
                if re.search(regex, search_text):
                    print(f"{filename}: enthält Begriffe")
                else:
                    print(f"{filename}: enthält nicht alle Begriffe")



        a = a+1

    i = i+1



