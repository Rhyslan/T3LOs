# Filename: utils.py
# Author: Rhyslan
# Created: 26/09/2026
# Description: Utilities for managing the bot

import joblib
from pathlib import Path
import discord


BASE_DIR = Path(__file__).resolve().parent


def create_secrets_file(file_path: Path):
    token = input("Discord bot token: ")
    guild_id = input("Discord server ID: ")

    file_path.write_text(
        f'TOKEN = "{token}"\n'
        f'MY_GUILD = "{guild_id}"',
        encoding="utf-8"
    )

    print("secrets.py created")

def add_admin(admin_list):
    print("Current admins:")
    print(admin_list)

    print("New admin information:")
    new_id = input("Discord User ID: ")
    new_name = input("Discord Username: ")

    admin_list.append([int(new_id), new_name])

    print("Added new admin")

    try:
        joblib.dump(admin_list, BASE_DIR / "data/admins.pkl")
        print("Admins updated")
        print("Current admins:")
        print(admin_list)
    except Exception as e:
        print(e)

def remove_admin(admin_list):
    if len(admin_list) <= 1:
        print("1 or less admins registered, unable to remove an admin")
        return

    print("Current admins:")
    print(admin_list)

    print("Existing admin information:")
    existing_id = input("Discord User ID: ")
    existing_name = input("Discord Username: ")

    admin_list.remove([int(existing_id), existing_name])

    print("Removed admin")

    try:
        joblib.dump(admin_list, BASE_DIR / "data/admins.pkl")
        print("Admins updated")
        print("Current admins:")
        print(admin_list)
    except Exception as e:
        print(e)

def clear_all_commands(token):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        guilds = [guild.id for guild in client.guilds]
        print(f'The {client.user.name} bot is in {len(guilds)} Guilds.\nThe guilds IDs list: {guilds}')
        for guildId in guilds:
            guild = discord.Object(id=guildId)
            print(f'Deleting commands from {guildId}.....')
            tree.clear_commands(guild=guild, type=None)
            await tree.sync(guild=guild)
            print(f'Deleted commands from {guildId}!')
            continue
        print('Deleting global commands.....')
        tree.clear_commands(guild=None, type=None)
        await tree.sync(guild=None)
        print('Deleted global commands!')

        await client.close()

    client.run(token)
