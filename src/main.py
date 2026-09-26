# Filename: main.py
# Author: Rhyslan
# Created: 14/03/2026
# Description: Main script

import logging
import joblib
from pathlib import Path

from utils import create_secrets_file, add_admin, remove_admin, clear_all_commands

SECRETS_FILE = Path("data/secrets.py")

if not SECRETS_FILE.exists():
    print("secrets.py does not exist. Creating now...")
    create_secrets_file(SECRETS_FILE)

from data.secrets import TOKEN
from bot import create_client


BASE_DIR = Path(__file__).resolve().parent

handler = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode="w"
)

def main():
    print("Checking for admin list...")
    if not Path("data/admins.pkl").exists():
        add_admin([])
        print("Admin list created")

    while True:
        print(
            "1. Run bot\n"
            "2. Add admin\n"
            "3. Remove admin\n"
            "4. Clear commands from all servers"
        )
        selection = input("Select an action: ")

        if selection == "1":
            break

        match selection:
            case "2":
                admins = joblib.load(BASE_DIR / "data/admins.pkl")
                add_admin(admins)
            case "3":
                admins = joblib.load(BASE_DIR / "data/admins.pkl")
                remove_admin(admins)
            case "4":
                clear_all_commands(TOKEN)
            case _:
                print("Invalid selection")

    client = create_client()

    print("Starting Discord client...")

    client.run(
        TOKEN,
        log_handler=handler
    )

if __name__ == "__main__":
    main()
