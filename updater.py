import os
import re
import shlex
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

CURRENT_EXE = sys.executable


# =====================================================
# VALIDATE VERSION FORMAT
# =====================================================

def is_valid_version(version: str) -> bool:
    return bool(re.match(r"^v\d+\.\d+\.\d+$", version))


# =====================================================
# GET CURRENT VERSION
# =====================================================

def get_current_version() -> str:

    if not os.path.exists(VERSION_FILE):
        return "v1.0.0"

    with open(VERSION_FILE, "r") as f:
        version = f.read().strip()

    if not is_valid_version(version):
        return "v1.0.0"

    return version


# =====================================================
# SANITIZE PATH
# =====================================================

def safe_path(path: str) -> str:
    return shlex.quote(os.path.normpath(path))


# =====================================================
# CHECK UPDATE
# =====================================================

def check_update():

    try:

        print("Checking for updates...")

        response = requests.get(API_URL, timeout=10)

        if response.status_code != 200:
            print("No GitHub release found.")
            return

        data = response.json()

        latest_version = data.get("tag_name", "v1.0.0")
        current_version = get_current_version()

        print("Current Version:", current_version)
        print("Latest Version:", latest_version)

        if not is_valid_version(latest_version):
            print("Invalid latest version format, skipping.")
            return

        if latest_version == current_version:
            print("Already up to date.")
            return

        print("New update found:", latest_version)

        assets = data.get("assets", [])

        if not assets:
            print("No assets found in release.")
            return

        # FIND EXE — validate asset name strictly
        download_url = None

        for asset in assets:

            name = asset.get("name", "")

            if (
                name.lower().endswith(".exe")
                and name == os.path.basename(name)
                and ".." not in name
            ):
                download_url = asset["browser_download_url"]
                break

        if not download_url:
            print("No safe EXE found in release assets.")
            return

        apply_update(download_url, latest_version)

    except Exception as e:
        print("Updater Error:", e)


# =====================================================
# APPLY UPDATE
# =====================================================

def apply_update(url: str, version: str):

    print("Downloading update...")

    exe_dir    = os.path.dirname(os.path.abspath(CURRENT_EXE))
    current_exe = os.path.normpath(os.path.abspath(CURRENT_EXE))
    temp_exe   = os.path.normpath(os.path.join(exe_dir, "_update_temp.exe"))
    backup_exe = os.path.normpath(os.path.join(exe_dir, "_backup.exe"))
    batch_path = os.path.normpath(os.path.join(exe_dir, "_updater.bat"))

    # BLOCK PATH TRAVERSAL
    for p in [temp_exe, backup_exe, batch_path]:
        if not os.path.abspath(p).startswith(exe_dir):
            print("Security error: path traversal detected.")
            return

    # DOWNLOAD
    try:

        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(temp_exe, "wb") as f:

            for chunk in response.iter_content(chunk_size=8192):

                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total:
                        pct = int(downloaded / total * 100)
                        print(f"\rDownloading... {pct}%", end="", flush=True)

        print("\nDownload complete.")

    except Exception as e:
        print("Download failed:", e)

        if os.path.exists(temp_exe):
            os.remove(temp_exe)

        return

    # SAVE NEW VERSION
    with open(VERSION_FILE, "w") as f:
        f.write(version)

    # QUOTED PATHS FOR BATCH
    q_current = safe_path(current_exe)
    q_temp    = safe_path(temp_exe)
    q_backup  = safe_path(backup_exe)
    q_batch   = safe_path(batch_path)
    pid       = os.getpid()

    batch_script = f"""@echo off
echo Waiting for app to close...
timeout /t 2 /nobreak >nul

:waitloop
tasklist /fi "PID eq {pid}" 2>nul | find /i "NexCustoms" >nul
if not errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto waitloop
)

echo Replacing old version...
move /y {q_current} {q_backup}

if errorlevel 1 (
    echo Failed to backup old EXE.
    del {q_temp} >nul 2>&1
    del "%~f0"
    exit /b 1
)

move /y {q_temp} {q_current}

if errorlevel 1 (
    echo Failed to replace EXE. Restoring backup...
    move /y {q_backup} {q_current}
    del "%~f0"
    exit /b 1
)

echo Cleaning up...
del {q_backup} >nul 2>&1

echo Restarting app...
start "" {q_current}

echo Done.
del {q_batch}
"""

    with open(batch_path, "w") as f:
        f.write(batch_script)

    # LAUNCH BATCH SILENTLY
    subprocess.Popen(
        ["cmd.exe", "/c", batch_path],
        creationflags=subprocess.CREATE_NO_WINDOW,
        close_fds=True,
        shell=False
    )

    print("Update ready. Restarting...")
    time.sleep(1)

    sys.exit()