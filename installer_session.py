#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key
from rubpy import Client as RubikaClient


# ==========================================================
# PATHS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

DEFAULT_SESSION_NAME = "rubika_session"


# ==========================================================
# HELPERS
# ==========================================================
def session_exists(session_name: str) -> bool:
    """
    Check if rubpy session files exist.
    """
    possible_files = [
        Path(session_name),
        Path(f"{session_name}.session"),
        Path(f"{session_name}.sqlite"),
    ]

    return any(f.exists() for f in possible_files)


def save_session_to_env(session_name: str):
    """
    Save session name to .env file.
    """
    if not ENV_FILE.exists():
        ENV_FILE.touch()

    set_key(str(ENV_FILE), "RUBIKA_SESSION", session_name)
    print("✅ Session saved to .env")


def create_new_session(session_name: str):
    """
    Create new rubika session interactively.
    """
    print("\n🔐 Creating new Rubika session...\n")

    try:
        client = RubikaClient(name=session_name)

        # rubpy handles asking phone and code internally
        client.start()

        print("✅ Login successful.")
        client.disconnect()

    except Exception as e:
        print(f"\n❌ Session creation failed: {e}")
        sys.exit(1)


# ==========================================================
# MAIN LOGIC
# ==========================================================
def main():
    print("\n=== Rubika Session Setup ===\n")

    existing_session = os.getenv("RUBIKA_SESSION", DEFAULT_SESSION_NAME)

    if session_exists(existing_session):
        print(f"✔ Existing session detected: {existing_session}")

        choice = input("Use existing session? (y/n): ").strip().lower()

        if choice == "y":
            print("✅ Using existing session.")
            save_session_to_env(existing_session)
            return

        else:
            print("⚠ Creating new session...")
            create_new_session(existing_session)
            save_session_to_env(existing_session)
            return

    else:
        print("No existing session found.")
        create_new_session(existing_session)
        save_session_to_env(existing_session)


if __name__ == "__main__":
    main()
