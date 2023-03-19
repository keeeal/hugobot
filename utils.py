from functools import partial
from random import choice
from typing import Any, Optional, TypeVar

from loguru import logger
from pyautogui import (FailSafeException, Point, center, click,
                       locateAllOnScreen, moveTo)

F = TypeVar("F")


def catch_failsafe(function: F) -> F:
    def _catch_failsafe(*args, **kwargs) -> Any:
        try:
            function(*args, **kwargs)
        except FailSafeException:
            logger.info("Exiting")

    return _catch_failsafe


def locate(image: str, verbose: bool = False) -> Optional[Point]:
    try:
        return center(next(locateAllOnScreen(image, limit=1)))
    except StopIteration:
        if verbose:
            logger.error(f"Could not find '{image}'")


def try_click(image: str, verbose: bool = True) -> Optional[Point]:
    if point := locate(image, verbose):
        click(point)

    return point


def reset_mouse():
    moveTo(1, 1)


last_watered_by_me = partial(locate, "assets/last-watered-by-me.png")
ready_to_be_watered = partial(locate, "assets/ready-to-be-watered.png")
fruit_is_falling = partial(locate, "assets/basket-button-green.png")
water_tree = partial(try_click, "assets/water-button-blue.png")
refresh_tree = partial(try_click, "assets/refresh-button-grey.png")
refresh_screen = partial(click, 800, 1000)


def catch_fruit(x: float, y: float, dx: float = 72, n: int = 5) -> None:
    points = [Point(x + i * dx, y) for i in range(n)]
    click(choice(points))
