import math
import random
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


# ---------------------------------------------------------------------------
# Geometry helpers — everything is in VIEWPORT coordinates (CSS pixels),
# which is what WebDriver pointer actions use. element.location is DOCUMENT
# coordinates and breaks as soon as the page scrolls, so it is never used.
# ---------------------------------------------------------------------------
def viewport_size(driver):
    w, h = driver.execute_script("return [window.innerWidth, window.innerHeight];")
    return int(w), int(h)


def clamp(x, y, w, h):
    return max(1, min(int(round(x)), w - 2)), max(1, min(int(round(y)), h - 2))


def get_rect(driver, el):
    return driver.execute_script(
        "const r = arguments[0].getBoundingClientRect();"
        "return {x: r.left, y: r.top, width: r.width, height: r.height};",
        el,
    )


def wait_until_still(driver, el, timeout=5.0, interval=0.1):
    """Wait until the element and page scrolling have settled."""
    deadline = time.time() + timeout
    last_state = None
    stable = 0

    while time.time() < deadline:
        state = tuple(driver.execute_script(
            """
            const r = arguments[0].getBoundingClientRect();
            return [
                r.left, r.top, r.width, r.height,
                window.scrollX, window.scrollY
            ];
            """,
            el,
        ))

        if state == last_state:
            stable += 1
            if stable >= 3:
                break
        else:
            stable = 0

        last_state = state
        time.sleep(interval)

    return get_rect(driver, el)


def is_in_view(rect, w, h, margin):
    top, bottom = rect["y"], rect["y"] + rect["height"]
    if rect["height"] > h - 2 * margin:  # taller than viewport: just need the top visible
        return margin <= top <= h - margin
    return top >= margin and bottom <= h - margin


def scroll_into_view(driver, el, mouse_pos, margin=60):
    """Scroll with the mouse wheel at the cursor's position, like a person would.
    The cursor itself does not move while scrolling, so mouse_pos stays valid."""
    w, h = viewport_size(driver)
    rect = get_rect(driver, el)
    no_progress = 0
    for _ in range(40):
        if is_in_view(rect, w, h, margin):
            break
        delta = (rect["y"] + rect["height"] / 2) - h / 2
        step = int(math.copysign(min(abs(delta), random.randint(80, 140)), delta))
        if step == 0:
            break
        ActionChains(driver).scroll_from_origin(
            ScrollOrigin.from_viewport(*mouse_pos), 0, step
        ).perform()
        time.sleep(random.uniform(0.03, 0.09))
        new_rect = get_rect(driver, el)
        no_progress = no_progress + 1 if abs(new_rect["y"] - rect["y"]) < 1 else 0
        rect = new_rect
        if no_progress >= 3:  # page can't scroll further (or wheel is captured)
            break

    rect = wait_until_still(driver, el)
    if not is_in_view(rect, w, h, margin):
        # Fallback: instant JS scroll, then re-measure
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        rect = wait_until_still(driver, el)
    return rect


def pick_point(driver, el, rect):
    """Random point inside the element that actually hits the element
    (not an overlay, label, or something covering it)."""
    for _ in range(12):
        px, py = rect["width"] * 0.2, rect["height"] * 0.25
        x = int(random.uniform(rect["x"] + px, rect["x"] + rect["width"] - px))
        y = int(random.uniform(rect["y"] + py, rect["y"] + rect["height"] - py))
        if hits_element(driver, el, x, y):
            return x, y
    return int(rect["x"] + rect["width"] / 2), int(rect["y"] + rect["height"] / 2)


def hits_element(driver, el, x, y):
    return driver.execute_script(
        "const t = document.elementFromPoint(arguments[1], arguments[2]);"
        "return !!t && (t === arguments[0] || arguments[0].contains(t));",
        el, x, y,
    )
