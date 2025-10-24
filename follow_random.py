import os
import random
import time

import pyautogui

from chrome import launch_chrome
from constants import DEADSPACE, IMAGE_REC_TOLERANCE, SCROLL_PAUSE_TIME, SEARCH_BAR_COORD
from csv_logger import OperationLogger
from image_rec import find_image
from logger import setup_logger
from window import focus_chrome_window

logger = setup_logger()
csv_logger = OperationLogger()


def get_random_target() -> str:
    fp = "data/target_profiles.txt"
    with open(fp, "r") as f:
        profiles = f.read().splitlines()
    return random.choice(profiles)


def convert_to_followers_url(random_target_url: str) -> str:
    return f"{random_target_url}/followers"


def get_to_followers_page(followers_page_url: str) -> None:
    focus_chrome_window()
    pyautogui.click(SEARCH_BAR_COORD)
    time.sleep(0.2)
    pyautogui.press("delete")
    time.sleep(0.2)
    pyautogui.write(followers_page_url)
    pyautogui.press("enter")
    time.sleep(7)


def find_random_follow_button() -> tuple[int, int] | None:
    all_found_coords = []
    reference_image_path = r"assets/follow_button_images"
    for image in os.listdir(reference_image_path):
        path = os.path.join(reference_image_path, image)
        base_image = pyautogui.screenshot()
        coords = find_image(base_image, path, tolerance=IMAGE_REC_TOLERANCE)
        all_found_coords.extend(coords)

    logger.info(f"Found {len(all_found_coords)} coords for follow buttons")
    if len(all_found_coords) > 0:
        coord = random.choice(all_found_coords)
        logger.info(f"Using this follow button coord: {coord}")
        return coord

    return None


def scroll_random() -> None:
    pyautogui.moveTo(*DEADSPACE, duration=0.1)
    random_scroll_amount = random.randint(500, 1000)
    pyautogui.scroll(-random_scroll_amount)
    time.sleep(SCROLL_PAUSE_TIME)
    time.sleep(1)


def follow_random(count: int = 1) -> None:
    logger.info(f"=== FOLLOW OPERATION STARTED === Target: {count} users")
    follows = 0
    while 1:
        random_target = get_random_target()
        logger.info(f"Random target selected: {random_target}")
        followers_page_url = convert_to_followers_url(random_target)
        logger.info(f"Navigating to followers page: {followers_page_url}")
        get_to_followers_page(followers_page_url)
        scroll_random()

        random_follow_button = find_random_follow_button()
        if random_follow_button:
            pyautogui.click(random_follow_button)
            follows += 1
            logger.info(f"[FOLLOW] Successfully followed user from {random_target}. Total follows this session: {follows}/{count}")
            csv_logger.log_operation(
                operation='follow',
                success=True,
                target_profile=random_target,
                details=f"Followed user at coordinates {random_follow_button}",
                session_total=follows
            )
        else:
            logger.warning(f"[FOLLOW] No follow button found on {random_target}")
            csv_logger.log_operation(
                operation='follow',
                success=False,
                target_profile=random_target,
                details="No follow button found on page",
                session_total=follows
            )

        if follows >= count:
            logger.info(f"=== FOLLOW OPERATION COMPLETED === Total followed: {count} users")
            break


if __name__ == "__main__":
    launch_chrome(url="https://example.com", incognito=False)
    follow_random(count=3)
