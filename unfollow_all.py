import os
import time

import pyautogui

from chrome import launch_chrome
from csv_logger import OperationLogger
from logger import setup_logger
from constants import (
    BASE_UNFOLLOW_URL,
    DEADSPACE,
    DUPE_COORD_TOL,
    IMAGE_REC_TOLERANCE,
    SCROLL_PAUSE_TIME,
    SEARCH_BAR_COORD,
    UNFOLLOW_CLICK_TIMEOUT,
)
from image_rec import find_image
from window import focus_chrome_window, scroll_page

logger = setup_logger()
csv_logger = OperationLogger()


def get_to_unfollow_page() -> None:
    pyautogui.click(SEARCH_BAR_COORD)
    pyautogui.press("delete")
    pyautogui.write(BASE_UNFOLLOW_URL)
    pyautogui.press("enter")


def remove_duplicate_coords(coords: list[tuple[int, int]], tolerance: float = DUPE_COORD_TOL) -> list[tuple[int, int]]:
    """
    Remove duplicate coordinates that are within tolerance distance of each other.

    Args:
        coords: List of (x, y) tuples
        tolerance: Euclidean distance threshold for considering coords as duplicates

    Returns:
        List of unique coordinates
    """
    if not coords:
        return []

    unique_coords = []

    for coord in coords:
        is_duplicate = False
        for existing in unique_coords:
            distance = (
                (coord[0] - existing[0]) ** 2 + (coord[1] - existing[1]) ** 2
            ) ** 0.5
            if distance < tolerance:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_coords.append(coord)

    return unique_coords


def find_all_unfollow_buttons() -> list[tuple[int, int]]:
    base_image = pyautogui.screenshot()
    reference_image_folder = r"assets/unfollow_button_images"

    all_button_coords = []

    if os.path.exists(reference_image_folder):
        for image_file in os.listdir(reference_image_folder):
            if image_file.endswith((".png", ".jpg", ".jpeg")):
                reference_path = os.path.join(reference_image_folder, image_file)
                coords = find_image(base_image, reference_path, IMAGE_REC_TOLERANCE)
                all_button_coords.extend(coords)

    all_button_coords = remove_duplicate_coords(
        all_button_coords, tolerance=DUPE_COORD_TOL
    )

    return all_button_coords


def find_confirm_unfollow_button() -> tuple[int, int] | None:
    base_image = pyautogui.screenshot()
    reference_image_folder = r"assets/confirm_unfollow_button_images"

    all_button_coords = []

    if os.path.exists(reference_image_folder):
        for image_file in os.listdir(reference_image_folder):
            if image_file.endswith((".png", ".jpg", ".jpeg")):
                reference_path = os.path.join(reference_image_folder, image_file)
                coords = find_image(base_image, reference_path, IMAGE_REC_TOLERANCE)
                all_button_coords.extend(coords)

    if all_button_coords:
        logger.info(f"Found {len(all_button_coords)} confirm button candidates")
        return all_button_coords[0]

    return None


def click_all_unfollow_buttons(button_coords: list[tuple[int, int]], session_total: int) -> int:
    count = 0
    confirm_button_coord = None

    for i, coord in enumerate(button_coords, 1):
        pyautogui.click(coord)
        time.sleep(UNFOLLOW_CLICK_TIMEOUT)

        if confirm_button_coord is None:
            logger.info("Searching for confirm unfollow button...")
            confirm_button_coord = find_confirm_unfollow_button()

            if confirm_button_coord is None:
                logger.warning("[UNFOLLOW] Confirm button not found! Clicking deadspace and waiting 60 seconds...")
                pyautogui.click(*DEADSPACE)
                csv_logger.log_operation(
                    operation='unfollow',
                    success=False,
                    target_profile='',
                    details=f"Confirm button not found for unfollow at {coord}",
                    session_total=session_total + count
                )
                time.sleep(60)
                continue
            else:
                logger.info(f"[UNFOLLOW] Confirm button found at {confirm_button_coord}, will reuse for batch")

        pyautogui.click(confirm_button_coord)
        pyautogui.moveTo(*DEADSPACE, duration=0.1)
        time.sleep(UNFOLLOW_CLICK_TIMEOUT)
        count += 1
        logger.info(f"[UNFOLLOW] Clicked unfollow button {i}/{len(button_coords)} at position {coord}")
        csv_logger.log_operation(
            operation='unfollow',
            success=True,
            target_profile='',
            details=f"Unfollowed user at coordinates {coord}, confirm at {confirm_button_coord}",
            session_total=session_total + count
        )
    return count


def main() -> None:
    logger.info("=== UNFOLLOW OPERATION STARTED ===")
    time.sleep(3)

    focus_chrome_window()
    time.sleep(1)
    get_to_unfollow_page()
    time.sleep(3)

    total_unfollowed = 0
    zero_found_counter = 0

    while True:
        pyautogui.moveTo(*DEADSPACE, duration=0.1)
        logger.info("Searching for unfollow buttons...")
        time.sleep(1)
        button_coords = find_all_unfollow_buttons()

        current_count = len(button_coords)

        if current_count == 0:
            zero_found_counter += 1
            logger.warning(f"[UNFOLLOW] No unfollow buttons found. ({zero_found_counter}/3)")
            if zero_found_counter >= 3:
                logger.info("[UNFOLLOW] No buttons found after 3 attempts. Done.")
                break
        else:
            zero_found_counter = 0
            logger.info(f"[UNFOLLOW] Found {current_count} unfollow buttons on screen.")

        logger.info(f"[UNFOLLOW] Clicking {current_count} unfollow buttons...")
        unfollowed_this_batch = click_all_unfollow_buttons(button_coords, total_unfollowed)
        total_unfollowed += unfollowed_this_batch
        logger.info(f"[UNFOLLOW] Progress: {total_unfollowed} users unfollowed so far")

        logger.info("Scrolling down to load more...")
        scroll_page()
        time.sleep(1)
        pyautogui.moveTo(*DEADSPACE, duration=0.1)

    logger.info(f"=== UNFOLLOW OPERATION COMPLETED === Total unfollowed: {total_unfollowed} users")


if __name__ == "__main__":
    launch_chrome(url="https://example.com", incognito=False)
    time.sleep(3)
    main()
