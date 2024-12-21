from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time
import shutil
from datetime import datetime

# Clean Up Temporary Files
shutil.rmtree("/tmp/.com.google.Chrome", ignore_errors=True)

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
print("1. Setting up Chrome options...")
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--lang=de-DE')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

print("2. Setting up ChromeDriver service...")
service = Service(ChromeDriverManager().install())

print("3. Initializing WebDriver...")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

print("4. Open the website")
driver.get("https://trends.google.com/trending?geo=DE&hours=24&status=active")

time.sleep(5)  # Wait for the page to load completely

# Define the container for the data
trending_data = []

print("5. Locate all rows on the page")
rows = driver.find_elements(By.CSS_SELECTOR, "tr")  # Assuming the data is in table rows

print("6. Extract data for each row")
for row in rows:
    try:
        angesagt = row.find_element(By.XPATH, ".//td[2]").text
        suchvolumen = row.find_element(By.XPATH, ".//td[3]").text
        gestartet = row.find_element(By.XPATH, ".//td[4]").text
        trendaufschluesselung = row.find_element(By.XPATH, ".//td[5]").text

        # Append to the data container
        trending_data.append({
            "Angesagt": angesagt,
            "Suchvolumen": suchvolumen,
            "Gestartet": gestartet,
            "Trendaufschluesselung": trendaufschluesselung,
        })
    except Exception as e:
        print(f"Error processing row: {e}")

# Add a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
data_with_timestamp = {
    "timestamp": timestamp,
    "trending_data": trending_data
}

print("7. Save the data to a JSON file")
output_file = "trending_data_raw.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data_with_timestamp, file, ensure_ascii=False, indent=4)

print(f"Data saved to {output_file}")

print("8. Print JSON")
json_string = json.dumps(data_with_timestamp, ensure_ascii=False, indent=4)
print(json_string)

# Close the driver
driver.quit()
