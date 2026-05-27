import os
import sys
import shlex
import subprocess

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from updater import check_update


URL = "https://nexcustoms-1036877213685.asia-east1.run.app/"

APP_PROFILE_DIR = os.path.normpath(
    os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
        "NexCustomsProfile"
    )
)

KNOWN_BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
]


# =====================================================
# FIND BROWSER
# =====================================================

def find_browser():

    for browser in KNOWN_BROWSERS:

        resolved = os.path.normpath(browser)

        if os.path.isabs(resolved) and os.path.exists(resolved):
            return resolved

    return None


# =====================================================
# LAUNCH APP
# =====================================================

def launch_app():

    browser = find_browser()

    if not browser:
        print("No supported browser found.")
        return

    os.makedirs(APP_PROFILE_DIR, exist_ok=True)

    args = [
        browser,
        f"--app={URL}",
        f"--user-data-dir={APP_PROFILE_DIR}",
        "--disable-infobars",
        "--disable-session-crashed-bubble",
        "--disable-notifications",
        "--disable-popup-blocking",
        "--disable-features=TranslateUI",
        "--no-first-run",
        "--force-dark-mode",
        "--window-size=1400,900",
        "--window-position=150,50",
    ]

    subprocess.Popen(
        args,
        shell=False
    )


# =====================================================
# START
# =====================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon("assets/logo.ico")
    )

    check_update()

    launch_app()

    sys.exit()