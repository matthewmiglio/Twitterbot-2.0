import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

from logger import setup_logger

logger = setup_logger()


def find_chrome_executable() -> str | None:
    """
    Try to locate Google Chrome/Chromium on Windows, macOS, and Linux.
    Returns the absolute path to the executable, or None if not found.
    """
    system = platform.system()

    # 1) Try PATH first
    candidates_on_path = [
        "google-chrome-stable",
        "google-chrome",
        "chrome",
        "chromium-browser",
        "chromium",
    ]
    for name in candidates_on_path:
        p = shutil.which(name)
        if p:
            return p

    # 2) Common install locations by OS
    if system == "Windows":
        possible_dirs = [
            os.environ.get("PROGRAMFILES", r"C:\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
            os.environ.get(
                "LOCALAPPDATA", r"C:\Users\{}\AppData\Local".format(os.getlogin())
            ),
        ]
        suffix = r"Google\Chrome\Application\chrome.exe"
        for base in possible_dirs:
            chrome_path = Path(base) / suffix
            if chrome_path.exists():
                return str(chrome_path)

    elif system == "Darwin":  # macOS
        mac_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            str(
                Path.home()
                / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ),
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
        for p in mac_paths:
            if Path(p).exists():
                return p

    else:  # Linux/Unix
        linux_paths = [
            "/usr/bin/google-chrome-stable",
            "/usr/bin/google-chrome",
            "/usr/local/bin/google-chrome",
            "/snap/bin/chromium",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ]
        for p in linux_paths:
            if Path(p).exists():
                return p

    return None


def kill_existing_chrome() -> None:
    """
    Force-terminate all running Chrome processes (best-effort).
    WARNING: This will close all Chrome windows and may interrupt active sessions.
    """
    system = platform.system()
    try:
        if system == "Windows":
            # /F = force, /IM = image name, /T = terminate child processes
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe", "/T"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif system == "Darwin":
            # macOS: kill Google Chrome & Chromium if present
            subprocess.run(
                ["pkill", "-f", "Google Chrome"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["pkill", "-f", "Chromium"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            # Linux
            # Try common process names
            for name in [
                "chrome",
                "google-chrome",
                "google-chrome-stable",
                "chromium",
                "chromium-browser",
            ]:
                subprocess.run(
                    ["pkill", "-f", name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
    except Exception:
        # Best-effort; ignore errors if nothing to kill or permissions are limited.
        pass


def launch_chrome(
    url: str | None = None, incognito: bool = False, user_data_dir: str | None = None
) -> subprocess.Popen | None:
    """
    Kills existing Chrome instances, then launches a fresh one.
    Returns the Popen object for the Chrome process (or None if Chrome not found).

    Args:
        url: Optional URL to open on launch.
        incognito: Launch in incognito mode if True.
        user_data_dir: Path to a profile directory (launches with that profile).
    """
    chrome_path = find_chrome_executable()
    if not chrome_path:
        logger.error("Chrome executable not found. Please install Chrome or add it to PATH.")
        return None

    # 1) Clear any running instances
    kill_existing_chrome()

    # 2) Build args
    args = [chrome_path]
    if incognito:
        args.append("--incognito")
    if user_data_dir:
        args.append(f"--user-data-dir={user_data_dir}")
    if url:
        args.append(url)

    # On macOS, launching .app binary sometimes prefers 'open -a' but direct exec works with the true path above.
    try:
        # Start detached where reasonable
        creationflags = 0
        start_new_session = False
        if platform.system() == "Windows":
            creationflags = (
                subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
            )
        else:
            start_new_session = True

        return subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags if platform.system() == "Windows" else 0,
            start_new_session=start_new_session,
        )
    except Exception as e:
        logger.error(f"Failed to launch Chrome: {e}")
        return None


# Example usage:
if __name__ == "__main__":
    proc = launch_chrome(url="https://example.com", incognito=False)
    if proc:
        logger.info("Chrome launched.")
