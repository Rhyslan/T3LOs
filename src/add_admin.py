# Filename: secrets.py
# Author: Dylan Musgrave
# Created: 14/03/2026
# Description: Basic script to add new admin user to the bot

import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    admins = joblib.load(BASE_DIR/"data/admins.pkl")
except Exception as e:
    print(e)
    admins = []

if __name__ == '__main__':
    print("current admins:")
    print(admins)

    if input("Add (1) or remove (2)?") == "1":
        new_id = input("User ID: ")
        new_name = input("User Name: ")

        admins.append([int(new_id), new_name])

        print("added new admin")
    else:
        new_id = input("User ID: ")
        new_name = input("User Name: ")

        admins.remove([int(new_id), new_name])

        print("removed admin")

    try:
        joblib.dump(admins, BASE_DIR/"data/admins.pkl")
        print("admins updated")
        print("current admins:")
        print(admins)
    except Exception as e:
        print(e)
