import os
import requests
import subprocess
import sys


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
# CHECK FOR UPDATE
# =====================================================

def check_update():

    try:

        response = requests.get(API_URL)

        data = response.json()

        latest_version = data["tag_name"]

        current_version = get_current_version()

        print("Current:", current_version)

        print("Latest:", latest_version)

        if latest_version != current_version:

            print("New update found.")

            assets = data["assets"]

            if len(assets) == 0:

                return

            download_url = assets[0][
                "browser_download_url"
            ]

            download_update(
                download_url,
                latest_version
            )

    except Exception as e:

        print("Update Error:", e)


# =====================================================
# DOWNLOAD UPDATE
# =====================================================

def download_update(url, version):

    exe_file = "NexCustoms_Update.exe"

    response = requests.get(
        url,
        stream=True
    )

    with open(exe_file, "wb") as file:

        for chunk in response.iter_content(
            chunk_size=8192
        ):

            if chunk:

                file.write(chunk)

    # SAVE NEW VERSION
    with open(VERSION_FILE, "w") as f:

        f.write(version)

    print("Update Downloaded")

    subprocess.Popen([exe_file])

    sys.exit()