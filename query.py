import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

def search(searchstring):
  # API-Schlüssel aus Umgebungsvariablen laden
  api_key = os.environ.get("EXA_API_KEY")
  if api_key is None:
    raise ValueError("EXA_API_KEY environment variable is not set")
  # Get current time in UTC
  now = datetime.now(pytz.UTC)
  yesterday = now - timedelta(hours=24)

  # Format as ISO 8601 with UTC timezone indicator (Z)
  end_date = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
  start_date = yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

  url = "https://api.exa.ai/search"

  payload = {
    "query": "What happened: " + searchstring,
    "type": "keyword",
    "numResults": 5,
    "excludeDomains": ["instagram.com"],
    "startCrawlDate": start_date,
    "endCrawlDate": end_date,
    "startPublishedDate": start_date,
    "endPublishedDate": end_date,
    "contents": {
      "text": {
        "maxCharacters": 1024,
        "includeHtmlTags": False
      }
    }
  }
  headers = {
      "x-api-key": api_key,
      "Content-Type": "application/json"
  }

  response = requests.request("POST", url, json=payload, headers=headers)

  return json.loads(response.text)

def main():
  # Umgebungsvariablen aus .env-Datei laden
  load_dotenv()
  
  json_data = search("bernburg")
  print(json.dumps(json_data))


if __name__ == "__main__":
  main()