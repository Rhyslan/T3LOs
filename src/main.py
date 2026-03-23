# Filename: main.py
# Author: Dylan Musgrave
# Created: 14/03/2026
# Description: Main bot script

import logging
import random
from pathlib import Path

import datetime
import discord
import joblib
import pandas as pd
from discord import app_commands

from data.secrets import TOKEN, MY_GUILD

import csv

BASE_DIR = Path(__file__).resolve().parent
DEBUG = True

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

class MinuteMaster(discord.Client):
    def __init__(self, *, intents: discord.Intents, task_list):
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

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=MY_GUILD))
        await self.tree.sync(guild=discord.Object(id=MY_GUILD))


intents = discord.Intents.default()
intents.message_content = True
tasks_file = open("data/tasks.csv")
csv_reader = csv.DictReader(tasks_file)
client = MinuteMaster(intents=intents, task_list=list(csv_reader))
tasks_file.close()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

@client.tree.command(name="join_game", description="Add yourself to the list of players")
async def join_game(interaction: discord.Interaction):
    """
    Only add user as play if they aren't already
    """
    if not [x for x in client.players if x["user"] == interaction.user]:
        client.players.append({"user": interaction.user, "answered?": False})
        await interaction.response.send_message(f"You have successfully been added to the list of players!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You are already a player", ephemeral=True)

@client.tree.command(name="leave_game", description="Remove yourself to the list of players")
async def leave_game(interaction: discord.Interaction):
    """
    Only remove user from players if they aren't already
    """
    if [x for x in client.players if x["user"] == interaction.user]:
        client.players = [x for x in client.players if x["user"] != interaction.user]
        await interaction.response.send_message(f"You have successfully been removed to the list of players!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You are not currently a player", ephemeral=True)

@client.tree.command(name="run_task", description="Let admins run a task now")
async def run_task(interaction: discord.Interaction):
    """
    Select new random task and send to all players
    """
    if len(client.players) <= 0:
        await interaction.response.send_message("There are no players", ephemeral=True)
        return

    try:
        # Only run if user is admin
        if [interaction.user.id, interaction.user.name] not in client.admins:
            await interaction.response.send_message("Only app admins can run this command", ephemeral=True)
        else:
            await interaction.response.defer(ephemeral=True)

            # Select new random task
            if len(client.available_tasks) > 0:
                client.current_task = random.choice(client.available_tasks)
                client.available_tasks = [item for item in client.available_tasks if item != client.current_task]
            else:
                # Reset tasks when run out
                client.task_list = client.available_tasks
                client.current_task = random.choice(client.available_tasks)
                client.available_tasks = [item for item in client.available_tasks if item != client.current_task]

            if DEBUG: print(f"Task {client.current_task} was chosen")

            if client.current_task["Has File"] == "true":
                for player in client.players:
                    player["answered?"] = False
                    due_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                    await player["user"].send(
                        f"{client.current_task["Task Description"]} Respond <t:{round(due_time.timestamp())}:R>",
                        file=discord.File(str(BASE_DIR) + "/" + client.current_task["File Path"]),
                        delete_after=60.0)
                    if DEBUG: print(f"Sent task {client.task_id} to {player["user"].name}")
            else:
                for player in client.players:
                    player["answered?"] = False
                    due_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                    await player["user"].send(
                        f"{client.current_task["Task Description"]} Respond <t:{round(due_time.timestamp())}:R>",
                        delete_after=60.0)
                    if DEBUG: print(f"Sent task {client.task_id} to {player["user"].name}")

            await interaction.followup.send("Tasks have been sent", ephemeral=True)
    except Exception as e:
        print("The task failed to run due to the following error:")
        print(e)
        await interaction.response.send_message("Task failed, please retry", ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.guild:
        async for old_msg in message.channel.history(limit=2):
            if old_msg.author == client.user:
                if old_msg.content.startswith(f"{client.current_task['Task Description']}"):
                    if client.current_task["Answer"].lower() in message.content.lower():
                        await message.channel.send("Correct", delete_after=60.0)
                        client.players = [{"user": player["user"], "answered?": True}
                                          if player["user"] == message.author else player for player in client.players]
                    else:
                        await message.channel.send("Incorrect", delete_after=60.0)

#toggle random tasks

#help
@client.tree.command(name="help")
async def help_message(interaction: discord.Interaction):
    await interaction.response.send_message("This game requires players to respond to tasks within 1 minute of receiving them.\n" +
                                            "Use `/join_game` to register as a player, and `/leave_game` to withdraw.\n" +
                                            "Tasks may be sent at any time, so be ready.",
                                            ephemeral=True)

@client.tree.command(name="view_players", description="Let admins view current player list")
async def view_players(interaction: discord.Interaction):
    if [interaction.user.id, interaction.user.name] in client.admins:
        await interaction.response.send_message(client.players, ephemeral=True)
    else:
        await interaction.response.send_message("Only app admins can run this command", ephemeral=True)

if __name__ == "__main__":
    client.run(TOKEN, log_handler=handler)
