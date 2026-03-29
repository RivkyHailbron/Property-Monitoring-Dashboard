from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # בטלי את ה-comment אם את לא רוצה שהדפדפן יקפוץ
    return webdriver.Chrome(options=options)


def scrape_property_data(driver, url):
    driver.get(url)
    # המתנה לטעינת טבלת המקרים (ID מה-HTML שסיפקת)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.ID, "dgPropCases2")))

    inspections = []
    # שליפת כל השורות בטבלה
    rows = driver.find_elements(By.XPATH, "//table[@id='dgPropCases2']/tbody/tr")

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4:
            case_type = cells[1].text.strip()
            case_num = cells[2].text.strip()
            date_closed = cells[3].text.strip()

            # לוגיקה עסקית: אם אין תאריך סגירה, המקרה פתוח ודורש טיפול
            is_open = not date_closed or date_closed == "" or date_closed.isspace()

            inspections.append({
                "case_number": case_num,
                "type": case_type,
                "date_closed": date_closed if not is_open else "STILL OPEN",
                "status": "Open" if is_open else "Closed",
                "urgency": "High 🚨" if is_open else "Low"
            })

    return inspections


def close_driver(driver):
    driver.quit()