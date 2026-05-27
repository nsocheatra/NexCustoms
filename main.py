import os
import sys
import subprocess

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from updater import check_update


URL = "https://nexcustoms-1036877213685.asia-east1.run.app/"


# =====================================================
# FIND MAIN BROWSER
# =====================================================

def find_browser():

    browsers = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]

    for browser in browsers:

        if os.path.exists(browser):

            return browser

    return None


# =====================================================
# OPEN APP MODE
# =====================================================

def launch_app():

    browser = find_browser()

    if not browser:

        print("Browser not found.")
        return

    subprocess.Popen([

        browser,

        f"--app={URL}",

        # USE MAIN PROFILE
        "--profile-directory=Default",

        "--disable-infobars",

        "--disable-session-crashed-bubble",

        "--disable-notifications",

        "--disable-popup-blocking",

        "--disable-features=TranslateUI",

        "--no-first-run",

        "--force-dark-mode",

        "--window-size=1400,900",

        "--window-position=150,50",
    ])


# =====================================================
# START
# =====================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon("assets/logo.ico")
    )

    # CHECK UPDATE
    check_update()

    # OPEN APP
    launch_app()

    sys.exit()