import sys
import re


VERSION_FILE = "version.txt"


# =====================================================
# VALIDATE VERSION FORMAT
# =====================================================

def is_valid_version(version: str) -> bool:
    """Must match vX.Y.Z format"""
    return bool(re.match(r"^v\d+\.\d+\.\d+$", version))


# =====================================================
# GET VERSION
# =====================================================

def get_version() -> str:

    try:
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()

    except FileNotFoundError:
        return "not found"


# =====================================================
# SET VERSION
# =====================================================

def set_version(version: str):

    if not version.startswith("v"):
        version = f"v{version}"

    if not is_valid_version(version):
        print(f"Invalid version format: {version}")
        print("Expected format: v1.2.3")
        sys.exit(1)

    with open(VERSION_FILE, "w") as f:
        f.write(version)

    print(f"Version updated: {version}")


# =====================================================
# BUMP VERSION
# =====================================================

def bump_version(part: str):
    """Bump major, minor, or patch automatically."""

    current = get_version()

    if not is_valid_version(current):
        print(f"Cannot bump: current version '{current}' is invalid.")
        sys.exit(1)

    # Strip leading 'v'
    major, minor, patch = map(int, current[1:].split("."))

    if part == "major":
        major += 1
        minor = 0
        patch = 0

    elif part == "minor":
        minor += 1
        patch = 0

    elif part == "patch":
        patch += 1

    else:
        print(f"Unknown bump type: {part}")
        print("Use: major | minor | patch")
        sys.exit(1)

    new_version = f"v{major}.{minor}.{patch}"

    set_version(new_version)


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    # No args — show current version
    if len(sys.argv) < 2:
        print("Current version:", get_version())
        print()
        print("Usage:")
        print("  python set_version.py v1.2.0          # set exact version")
        print("  python set_version.py bump patch       # v1.0.0 → v1.0.1")
        print("  python set_version.py bump minor       # v1.0.0 → v1.1.0")
        print("  python set_version.py bump major       # v1.0.0 → v2.0.0")
        sys.exit(0)

    # Bump command
    if sys.argv[1] == "bump":

        if len(sys.argv) < 3:
            print("Usage: python set_version.py bump patch|minor|major")
            sys.exit(1)

        bump_version(sys.argv[2])

    # Set exact version
    else:
        set_version(sys.argv[1])