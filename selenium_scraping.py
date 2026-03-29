from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


def start_driver():
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)


def scrape_property_data(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # המתנה לטעינת הטבלה [cite: 24]
    wait.until(EC.presence_of_element_located((By.ID, "dgPropCases2")))

    try:
        # הצגת כל הרשומות (All) כדי לא לפספס מידע [cite: 45]
        length_menu = driver.find_element(By.NAME, "dgPropCases2_length")
        select = Select(length_menu)
        select.select_by_value("-1")
        time.sleep(3)
    except:
        pass

    inspections = []
    rows = driver.find_elements(By.XPATH, "//table[@id='dgPropCases2']/tbody/tr")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4:
            case_num = cells[2].text.strip()
            date_closed = cells[3].text.strip()

            # לוגיקה עסקית לניהול סטטוסים ודחיפות [cite: 14, 15, 16]
            is_closed = date_closed and date_closed != " " and date_closed != ""

            if is_closed:
                status = "Closed ✅"
                urgency = "Low"
            else:
                # בטיפול = מקרה חדש (2025/26). פתוח/דחוף = מקרה ישן ללא סגירה. [cite: 15, 16, 55]
                if "2025" in case_num or "2026" in case_num:
                    status = "In Progress ⚙️"
                    urgency = "Medium"
                else:
                    status = "Open 🔴"
                    urgency = "High 🚨"

            inspections.append({
                "case_type": cells[1].text.strip(),
                "case_number": case_num,
                "status": status,
                "urgency": urgency,
                "date_closed": date_closed if is_closed else "Pending",
                "is_new": "2026" in case_num  # אינדיקציה למה חדש [cite: 33]
            })

    return inspections


def close_driver(driver):
    if driver:
        driver.quit()