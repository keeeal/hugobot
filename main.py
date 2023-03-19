from itertools import count
from time import time
from typing import Optional

from fire import Fire
from loguru import logger
from pyautogui import Point
from tqdm import tqdm

from utils import (catch_failsafe, catch_fruit, fruit_is_falling,
                   last_watered_by_me, ready_to_be_watered, refresh_screen,
                   refresh_tree, reset_mouse, water_tree)


@catch_failsafe
def main():
    logger.info("Starting HugoBot...")
    last_refresh = 0
    last_water_point: Optional[Point] = None

    for _ in tqdm(count()):
        reset_mouse()

        if (t := time()) - last_refresh > 10:
            last_refresh = t
            if not refresh_tree():
                refresh_screen()

        elif fruit_point := fruit_is_falling() and last_water_point:
            print()
            logger.info("Catching fruit...")
            catch_fruit(last_water_point.x, fruit_point.y)

        elif ready_to_be_watered() and not last_watered_by_me():
            print()
            logger.info("Watering tree...")
            last_water_point = water_tree()


if __name__ == "__main__":
    Fire(main)
