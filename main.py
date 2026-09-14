from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    # Open your React app
    driver.get("http://localhost:5173/")

    wait = WebDriverWait(driver, 10)

    # Wait for and fill email
    email_input = wait.until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    time.sleep(2)
    email_input.send_keys("test@example.com")

    # Fill password
    password_input = driver.find_element(By.ID, "password")
    time.sleep(1)
    password_input.send_keys("mypassword123")

    # Submit the form
    login_button = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )
    time.sleep(1)
    login_button.click()

finally:
    # Keep browser open temporarily if you want to inspect results
    time.sleep(3)
    driver.quit()