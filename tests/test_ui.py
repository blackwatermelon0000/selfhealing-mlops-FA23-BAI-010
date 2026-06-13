import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
            EC.presence_of_element_located((By.ID, "text-input"))
        )
        text_input.send_keys("A masterpiece of storytelling with complex characters and beautifully crafted prose")
        driver.find_element(By.ID, "submit-btn").click()

        result = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "result-output"))
        )

        output = result.text.strip()
        assert output != ""
        assert ("POSITIVE" in output) or ("NEGATIVE" in output) or ("Confidence" in output)
    finally:
        driver.quit()
