from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_full_flow():
    url = "https://housingapp.lacity.org/reportviolation/Pages/PropAtivityCases?APN=2654002037&Source=ActivityReport"

    print("🚀 מתחילים בדיקה... פותח דפדפן")
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # שלב 1: וודוא שהטבלה נטענה
        print("⏳ ממתין לטעינת הטבלה...")
        wait.until(EC.presence_of_element_located((By.ID, "dgPropCases2")))
        print("✅ הטבלה נמצאה!")

        # שלב 2: חילוץ נתונים בסיסי מהטבלה (בלי להיכנס פנימה עדיין)
        rows = driver.find_elements(By.XPATH, "//table[@id='dgPropCases2']/tbody/tr")
        print(f"📊 נמצאו {len(rows)} שורות בטבלה.")

        inspections = []
        for index, row in enumerate(rows[:5]):  # נבדוק רק את ה-5 הראשונים למהירות
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                case_num = cells[2].text.strip()
                status_date = cells[3].text.strip()
                # לוגיקה עסקית לזיהוי מה פתוח/דחוף [cite: 16, 33]
                is_open = not status_date or status_date == "" or status_date.isspace()

                print(f"🔎 בודק מקרה {case_num}: {'פתוח 🔴' if is_open else 'סגור ✅'}")

                inspections.append({
                    "number": case_num,
                    "status": "Open" if is_open else "Closed"
                })

        # שלב 3: בדיקת לחיצה על מקרה אחד כדי לראות אם הפרטים נפתחים
        if rows:
            print(f"🖱️ מנסה להקליק על המקרה הראשון ({inspections[0]['number']})...")
            select_button = rows[0].find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].click();", select_button)

            time.sleep(3)  # המתנה לטעינה של ה-Postback
            print("📄 בודק אם עמוד הפרטים נטען...")

            # בדיקה אם מופיע כפתור "Back" או אלמנט מהדף החדש
            if "Case Information" in driver.page_source or "PROPERTY INFORMATION" in driver.page_source:
                print("✨ הצלחה! הסלניום הצליח לנווט לפרטי המקרה.")
            else:
                print("⚠️ נראה שהדף לא השתנה כמצופה.")

    except Exception as e:
        print(f"❌ שגיאה במהלך הבדיקה: {e}")

    finally:
        print("🔒 סוגר דפדפן.")
        driver.quit()


if __name__ == "__main__":
    test_full_flow()