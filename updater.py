import os
import requests
import subprocess
import sys
import time


# =====================================================
# GITHUB CONFIG
# =====================================================

GITHUB_USER = "nsocheatra"

REPO_NAME = "NexCustoms"

API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_USER}/{REPO_NAME}/releases/latest"
)

VERSION_FILE = "version.txt"


# =====================================================
# GET CURRENT VERSION
# =====================================================

def get_current_version():

    if not os.path.exists(VERSION_FILE):

        return "1.0.0"

    with open(VERSION_FILE, "r") as f:

        return f.read().strip()


# =====================================================
# CHECK UPDATE
# =====================================================

def check_update():

    try:

        print("Checking for updates...")

        response = requests.get(API_URL)

        # NO RELEASE
        if response.status_code != 200:

            print("No GitHub release found.")
            return

        data = response.json()

        latest_version = data.get(
            "tag_name",
            "1.0.0"
        )

        current_version = (
            get_current_version()
        )

        print("Current Version:", current_version)

        print("Latest Version:", latest_version)

        # SAME VERSION
        if latest_version == current_version:

            print("Already latest version.")
            return

        print("New update found.")

        assets = data.get("assets", [])

        if len(assets) == 0:

            print("No EXE asset uploaded.")
            return

        # FIND EXE FILE
        download_url = None

        for asset in assets:

            name = asset["name"].lower()

            if name.endswith(".exe"):

                download_url = asset[
                    "browser_download_url"
                ]

                break

        if not download_url:

            print("No EXE found in release.")
            return

        download_update(
            download_url,
            latest_version
        )

    except Exception as e:

        print("Updater Error:", e)


# =====================================================
# DOWNLOAD UPDATE
# =====================================================

def download_update(url, version):

    print("Downloading update...")

    temp_file = "NexCustoms_Update.exe"

    response = requests.get(
        url,
        stream=True
    )

    with open(temp_file, "wb") as file:

        for chunk in response.iter_content(
            chunk_size=8192
        ):

            if chunk:

                file.write(chunk)

    print("Download Complete")

    # SAVE VERSION
    with open(VERSION_FILE, "w") as f:

        f.write(version)

    time.sleep(1)

    # OPEN UPDATED APP
    subprocess.Popen([temp_file])

    # CLOSE CURRENT APP
    sys.exit()