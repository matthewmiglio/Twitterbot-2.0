import time
from typing import Any

import pyautogui
import pygetwindow

from constants import DEADSPACE, SCROLL_AMOUNT, SCROLL_PAUSE_TIME


def print_active_titles() -> None:
    windows = pygetwindow.getAllWindows()
    for window in windows:
        if len(window.title) > 0:
            print(window.title)


def get_chrome_window() -> Any | None:
    substring = "Google Chrome"
    windows = pygetwindow.getAllWindows()
    for window in windows:
        if substring in window.title:
            return window
    return None


def scroll_page() -> None:
    pyautogui.moveTo(*DEADSPACE, duration=0.1)
    pyautogui.scroll(-1 * SCROLL_AMOUNT)
    time.sleep(SCROLL_PAUSE_TIME)


def focus_chrome_window() -> bool:
    chrome_window = get_chrome_window()
    if chrome_window:
        chrome_window.activate()
        return True
    return False


if __name__ == "__main__":
    print_active_titles()
    chrome_window = get_chrome_window()
    if chrome_window:
        print(f"Found Chrome window: {chrome_window.title}")
    else:
        print("Chrome window not found.")
    focus_chrome_window()
