import math
import random

from selenium.webdriver.common.actions.action_builder import ActionBuilder

from config import DEBUG_TRAIL
from debug_visuals import draw_debug_trail
from geometry import clamp, viewport_size


def calculate_bezier_point(p0, p1, p2, p3, t):
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )


def move_mouse_humanlike(driver, start, target):
    """Move along a Bezier curve using ABSOLUTE viewport positions, sent as one
    batched action. Returns the final (x, y)."""
    w, h = viewport_size(driver)
    sx, sy = start
    tx, ty = target

    dist = math.hypot(tx - sx, ty - sy)
    steps = max(8, min(45, int(dist / 12)))

    ox = (tx - sx) * random.uniform(0.1, 0.4)
    oy = (ty - sy) * random.uniform(0.1, 0.4)
    jitter = min(50, max(5, dist * 0.15))
    p1x = sx + ox + random.uniform(-jitter, jitter)
    p1y = sy + oy + random.uniform(-jitter, jitter)
    p2x = tx - ox + random.uniform(-jitter, jitter)
    p2y = ty - oy + random.uniform(-jitter, jitter)

    builder = ActionBuilder(driver)
    mouse = builder.pointer_action.source
    path, last = [], (sx, sy)
    for i in range(1, steps + 1):
        t = i / steps
        te = (1 - math.cos(math.pi * t)) / 2  # ease-in-out: accelerate, then slow down
        x = calculate_bezier_point(sx, p1x, p2x, tx, te)
        y = calculate_bezier_point(sy, p1y, p2y, ty, te)
        x, y = clamp(x, y, w, h)  # never leave the viewport -> no MoveTargetOutOfBounds
        if (x, y) == last:
            continue
        # duration is in ms; Selenium's default is 250ms PER MOVE, which made the old version crawl
        mouse.create_pointer_move(duration=random.randint(30, 50), x=x, y=y)
        path.append((x, y))
        last = (x, y)

    if last != (tx, ty):
        mouse.create_pointer_move(duration=random.randint(30, 50), x=tx, y=ty)
        path.append((tx, ty))
        last = (tx, ty)

    if path:
        builder.perform()
        if DEBUG_TRAIL:
            draw_debug_trail(driver, path)
    return last


def spawn_mouse(driver):
    w, h = viewport_size(driver)
    x, y = clamp(random.randint(300, 800), random.randint(100, 500), w, h)
    builder = ActionBuilder(driver)
    builder.pointer_action.source.create_pointer_move(duration=0, x=x, y=y)
    builder.perform()
    return x, y
