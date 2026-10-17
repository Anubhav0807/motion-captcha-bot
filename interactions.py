import random
import time

from selenium.webdriver.common.actions.action_builder import ActionBuilder

from config import DEBUG_TRAIL
from geometry import hits_element, pick_point, scroll_into_view, wait_until_still
from mouse_movement import move_mouse_humanlike


def mouse_click(driver):
    builder = ActionBuilder(driver)
    p = builder.pointer_action
    p.pointer_down()
    p.pause(random.uniform(0.05, 0.12))
    p.pointer_up()
    builder.perform()


def human_click(driver, mouse_pos, el):
    scroll_into_view(driver, el, mouse_pos)

    # Get the button's latest position after scrolling.
    rect = wait_until_still(driver, el)

    target = pick_point(driver, el, rect)
    mouse_pos = move_mouse_humanlike(driver, mouse_pos, target)
    time.sleep(random.uniform(0.08, 0.25))

    # Keep your existing layout-shift correction here.
    if not hits_element(driver, el, *mouse_pos):
        rect = wait_until_still(driver, el)
        target = pick_point(driver, el, rect)
        mouse_pos = move_mouse_humanlike(driver, mouse_pos, target)
        time.sleep(random.uniform(0.05, 0.15))

    mouse_click(driver)
    return mouse_pos


def type_humanlike(el, text):
    for char in text:
        el.send_keys(char)
        time.sleep(random.uniform(0.04, 0.16))
