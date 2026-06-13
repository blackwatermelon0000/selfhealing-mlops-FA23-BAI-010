import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

def test_frontend_sentiment():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(BASE_URL)

        text_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "text-input"))
        )

        text_input.clear()
        text_input.send_keys(
            "A masterpiece of storytelling with complex characters and beautifully crafted prose"
        )

        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "submit-btn"))
        )
        submit_btn.click()

        WebDriverWait(driver, 40).until(
            lambda d: d.find_element(By.ID, "result-output").text.strip() != ""
        )

        output = driver.find_element(By.ID, "result-output").text.strip()

        assert output != ""
        assert "POSITIVE" in output.upper() or "NEGATIVE" in output.upper()
    finally:
        driver.quit()
