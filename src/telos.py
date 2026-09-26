# Filename: telos.py
# Author: Rhyslan
# Created: 26/09/2026
# Description: Game discord client class

import re
from pathlib import Path

import discord
import joblib
from discord import app_commands

from data.secrets import MY_GUILD


BASE_DIR = Path(__file__).resolve().parent


class Telos(discord.Client):
    def __init__(self, *, intents: discord.Intents, task_list, code, encoded_code):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        try:
            self.admins = joblib.load(BASE_DIR/"data/admins.pkl")
        except Exception as e:
            print(e)
            self.admins = []

        self.players = []
        self.task_list = task_list
        self.available_tasks = task_list
        self.task_id = 0
        self.current_task = None

        self.code = code
        self.chunk_size = 8
        self.split_code = re.findall(".{1," + str(self.chunk_size) + "}", str(encoded_code))
        self.awaiting_code = False

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=MY_GUILD))
        await self.tree.sync(guild=discord.Object(id=MY_GUILD))