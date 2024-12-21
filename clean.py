import json

# Funktion, um die Rohdaten zu bereinigen und das gewünschte Format zu erzeugen
def process_trending_data(input_file, output_file):
    # Rohdaten einlesen
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)

    # Zeitstempel extrahieren
    timestamp = raw_data.get("timestamp", "")
    trending_data = raw_data.get("trending_data", [])

    cleaned_data = {
        "timestamp": timestamp,
        "trending_data": []
    }

    for entry in trending_data:
        # Suchvolumen bereinigen
        search_volume_raw = entry["Suchvolumen"].split("+\n")[0].strip()
        search_volume = search_volume_raw.replace("M", "000000").replace("K", "000")
        
        # Startzeitpunkt bereinigen
        started = entry["Gestartet"].split(" ")[0] + " " + entry["Gestartet"].split(" ")[1]
        
        # Trendaufschlüsselung bereinigen
        trend_details_raw = entry.get("Trendaufschluesselung", "")
        trend_details = [
            variant.strip() for variant in trend_details_raw.split("\n") if "+" not in variant
        ]

        # Bereinigten Eintrag erzeugen
        cleaned_entry = {
            "Angesagt": entry["Angesagt"],
            "Suchvolumen": search_volume,
            "Gestartet": started,
            "Trendaufschluesselung": trend_details
        }

        cleaned_data["trending_data"].append(cleaned_entry)

    # Bereinigte Daten speichern
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

# Dateinamen definieren
input_file = 'trending_data_raw.json'
output_file = 'trending_data_clean.json'

# Daten verarbeiten
process_trending_data(input_file, output_file)

print(f"Die bereinigten Daten wurden in '{output_file}' gespeichert.")
