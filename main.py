import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import CHROMEDRIVER_PATH, EMAIL, PASSWORD, attempts
from interactions import human_click, type_humanlike
from mouse_movement import spawn_mouse


service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

try:
    for attempt in range(1, attempts + 1):
        print(f"\n========== Attempt {attempt}/{attempts} ==========")

        driver.get("http://localhost:5173/")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        mouse_pos = spawn_mouse(driver)
        print(f"Mouse spawned at viewport coordinate: {mouse_pos}")

        # EMAIL
        email_input = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[role="textbox"][aria-label="Email address"]')
            )
        )
        mouse_pos = human_click(driver, mouse_pos, email_input)
        time.sleep(random.uniform(0.1, 0.3))
        type_humanlike(email_input, EMAIL)

        # PASSWORD
        password_input = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[role="textbox"][aria-label="Password"]')
            )
        )
        mouse_pos = human_click(driver, mouse_pos, password_input)
        time.sleep(random.uniform(0.1, 0.3))
        type_humanlike(password_input, PASSWORD)

        # SIGN IN
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        time.sleep(random.uniform(0.2, 0.5))
        mouse_pos = human_click(driver, mouse_pos, login_button)

        print("Login submitted")
        time.sleep(3)

finally:
    try:
        for _ in range(100):
            if not driver.window_handles:
                break
            time.sleep(1)
        else:
            driver.quit()
    except Exception:
        pass
