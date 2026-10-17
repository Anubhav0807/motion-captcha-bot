import random

CHROMEDRIVER_PATH = r"C:\WebDriver\chromedriver-win64\chromedriver.exe"

EMAIL = "test@example.com"
PASSWORD = "mypassword123"
DEBUG_TRAIL = True  # draw red dots along the cursor path


class Mode:
    TRAIN = "train"
    TEST = "test"


# Change the mode from here
mode = Mode.TEST

if mode == Mode.TRAIN:
    random.seed(42)
    attempts = 25
else:
    attempts = 1
