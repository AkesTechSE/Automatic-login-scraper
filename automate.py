from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# --- Use environment variables for safety ---
EMAIL = os.environ.get("EMAIL", "your_email")
PASSWORD = os.environ.get("PASSWORD", "your_password")

# --- Chrome setup ---
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # --- Open hosted React login page ---
    driver.get("https://localhost:5000/")  # Replace with your URL

    # --- Wait for login section ---
    login_section = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "inline-login"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", login_section)

    # --- Fill email & password ---
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD)

    # --- Press Enter to login ---
    password_input.send_keys(Keys.RETURN)

    # --- Wait for dashboard to load ---
    dashboard_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))  # or a unique dashboard element
    )
    time.sleep(2)

    # --- Scrape case cards (adjust CSS selector) ---
    cards = driver.find_elements(By.CSS_SELECTOR, ".MuiCard-root")  # adjust to your cards
    for i, card in enumerate(cards, 1):
        title = card.find_element(By.TAG_NAME, "h3").text
        desc = card.find_element(By.TAG_NAME, "p").text
        print(f"Case {i}: {title} - {desc}")

    print("Scraping complete. Logging out automatically...")

    # --- Automatic logout ---
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Logout']"))  # Replace with actual logout button
    )
    logout_button.click()
    print("Logged out successfully ✅")

    time.sleep(2)  # wait a bit before closing browser

finally:
    driver.quit()
