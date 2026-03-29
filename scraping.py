import json
from selenium_scraping import start_driver, scrape_property_data, close_driver

url = "https://housingapp.lacity.org/reportviolation/Pages/PropAtivityCases?APN=2654002037&Source=ActivityReport"

driver = start_driver()
try:
    print("Scraping data... please wait.")
    data = scrape_property_data(driver, url)

    # שמירה למבנה נתונים מסודר
    output = {
        "property_apn": "2654002037",
        "inspections": data
    }

    with open("inspections_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"Successfully scraped {len(data)} cases.")
finally:
    close_driver(driver)