from openai import OpenAI
import json
import os
from dotenv import load_dotenv

def load_system_definition(file_path='assistant.txt'):
    """Lädt die System-Definition aus der Textdatei."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warnung: Datei {file_path} nicht gefunden. Verwendung einer Standarddefinition.")
        return "Du bist ein Assistent für Trendanalyse."

def load_trending_data(file_path='trending_data_clean.json'):
    """Lädt die Trending Data aus der JSON-Datei."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Fehler: {file_path} nicht gefunden.")
        return None

def process_trending_data(system_definition, trending_data):
    """
    Verarbeitet einen einzelnen Trending Topic Eintrag 
    und transformiert ihn in das spezifizierte JSON-Format
    """
    try:
        # API-Schlüssel aus Umgebungsvariablen laden
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Fehler: ANTHROPIC_API_KEY nicht gesetzt.")
            return None

        # Client initialisieren
        client = OpenAI(api_key=api_key)

        # API-Anfrage
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_definition},
                {"role": "user", "content": json.dumps(trending_data, ensure_ascii=False)}
            ]
        )

        # Antwort als JSON parsen
        response_text = response.choices[0].message.content
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print(f"Konnte JSON nicht parsen. Rohe Antwort: {response_text}")
            return None

    except Exception as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        return None

def main():
    # Umgebungsvariablen aus .env-Datei laden
    load_dotenv()

    # Systemdefinition laden
    system_definition = load_system_definition()
    if not system_definition:
        return
    
    # Trending Data aus JSON-Datei laden
    trending_data = load_trending_data()
    if not trending_data:
        return
    
    # Verarbeitung der Trending Topics
    processed_trends = []
    total_topics = len(trending_data.get('trending_data', []))
    
    for i, trending_data_single in enumerate(trending_data.get('trending_data', []), 1):
        print(f"Verarbeite Trending Topic {i}/{total_topics}")
        print(f"Data raw: {trending_data_single}")
        processed_data = process_trending_data(system_definition, trending_data_single)
        print(f"Data processed: {processed_data}")

        if processed_data:
            processed_trends.append(processed_data)
        else:
            print(f"Fehler bei der Verarbeitung von Trending Topic {i}")
        
        if i == 10:
            break;
    
    # Speichern der verarbeiteten Daten
    output_data = {
        "timestamp": trending_data.get('timestamp', ''),
        "processed_trends": processed_trends
    }
    
    # Speichern in einer Ausgabedatei
    output_file = 'trending_data_processed_OpenAI.json'
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=2)
    
    print(f"Verarbeitung abgeschlossen. Ergebnisse in {output_file} gespeichert.")

if __name__ == "__main__":
    main()