from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(r"C:\WebDriver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

EMAIL = "test@example.com"
PASSWORD = "mypassword123"
ATTEMPTS = 25

try:
    for attempt in range(1, ATTEMPTS + 1):
        print(f"\n========== Attempt {attempt}/{ATTEMPTS} ==========")

        driver.get("http://localhost:5173/")

        wait = WebDriverWait(driver, 10)

        # -----------------------------------------
        # EMAIL
        # -----------------------------------------

        email_input = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[role="textbox"][aria-label="Email address"]')
            )
        )

        email_input.click()

        for char in EMAIL:
            email_input.send_keys(char)
            time.sleep(0.08)

        # -----------------------------------------
        # PASSWORD
        # -----------------------------------------

        password_input = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[role="textbox"][aria-label="Password"]')
            )
        )

        password_input.click()

        for char in PASSWORD:
            password_input.send_keys(char)
            time.sleep(0.08)

        # -----------------------------------------
        # SIGN IN
        # -----------------------------------------

        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[type="submit"]')
            )
        )

        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.move_to_element(login_button).click_and_hold().pause(0.06).release().perform()

        print("Login submitted")

        # Give React/backend time to process the request
        time.sleep(3)

finally:
    driver.quit()