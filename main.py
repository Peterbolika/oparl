import urllib.request
import json
import os
import re
import PyPDF2
import itertools

# Liste der zu suchenden Begriffe
regex = r"\b(Ausschuss für Gleichstellung|Ausschuss für Personal, Digitalisierung, Organisation|Ausschuss für Soziales, Gesundheit, Verbraucherschutz und Arbeitsförderung|Ausschuss für Stadtplanung und Stadtentwicklung|Ausschuss für Umweltschutz, Klimaschutz und Bauwesen|Ausschuss für Verkehr und Mobilität|Ausschuss für Wohnen, Liegenschaften, Finanzen und Wirtschaft|Kulturausschuss|Sportausschuss)\b"

pages = 25# insgesamt 1980
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
                search_text = pdf_reader.pages[0].extract_text()

                # Überprüfen, welcher Regex gefunden wurde
                matches = re.findall(regex, search_text)
                if matches:
                    results.append((filename, matches))

        a += 1

    i += 1

# Erstellen einer Liste aller möglichen Kombinationen von regex-Ausdrücken
combos = list(itertools.combinations(regex.split("|"), 2))
# Erstellen der Matrix

# Extrahieren der einzigartigen Begriffe aus der Ergebnisliste
unique_terms = list(set([term for result in results for term in result[1]]))

# Erstellen der Matrix als Dictionary
matrix = {}
for term in unique_terms:
    matrix[term] = [0] * len(unique_terms)

# Füllen der Matrix
for result in results:
    for i in range(len(result[1])):
        for j in range(i+1, len(result[1])):
            term1 = result[1][i]
            term2 = result[1][j]
            if term1 != term2:
                matrix[term1][unique_terms.index(term2)] += 1
                matrix[term2][unique_terms.index(term1)] += 1

# Ausgabe der Matrix
header = [''] + unique_terms
for i in range(len(unique_terms)+1):
    for j in range(len(unique_terms)+1):
        if i == 0 and j == 0:
            print("{:<80}".format(header[j]), end='')
        elif i == 0 and j != 0:
            print("{:<80}".format(header[j]), end='')
        elif i != 0 and j == 0:
            print("{:<80}".format(header[i]), end='')
        else:
            print("{:<80}".format(matrix[unique_terms[i-1]][j-1]), end='')
    print('\n')


