import datetime
import logging
import random
from pathlib import Path

import discord
import joblib
import pandas as pd
from discord import app_commands

from data.secrets import TOKEN, MY_GUILD

BASE_DIR = Path(__file__).resolve().parent
DEBUG = True

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

task_list = pd.read_csv(BASE_DIR/"data/tasks.csv")

class MinuteMaster(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        try:
            self.admins = joblib.load(BASE_DIR/"data/admins.pkl")
        except Exception as e:
            print(e)
            self.admins = []

        self.players = []
        self.task_start = datetime.datetime.now()
        self.task_end = self.task_start + datetime.timedelta(minutes=1)
        self.task_id = 0
        self.current_task = None

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=MY_GUILD))
        await self.tree.sync(guild=discord.Object(id=MY_GUILD))


intents = discord.Intents.default()
intents.message_content = True
client = MinuteMaster(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

@client.tree.command(name="join_game", description="Add yourself to the list of players")
async def join_game(interaction: discord.Interaction):
    if not [x for x in client.players if x[0] == interaction.user]:
        client.players.append([interaction.user, False])
        await interaction.response.send_message(f"You have successfully been added to the list of players!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You are already a player", ephemeral=True)

@client.tree.command(name="leave_game", description="Remove yourself to the list of players")
async def leave_game(interaction: discord.Interaction):
    if [x for x in client.players if x[0] == interaction.user]:
        client.players = [x for x in client.players if x[0] != interaction.user]
        await interaction.response.send_message(f"You have successfully been removed to the list of players!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You are not currently a player", ephemeral=True)

@client.tree.command(name="run_task", description="Let admins run a task now")
async def run_task(interaction: discord.Interaction):
    try:
        if [interaction.user.id, interaction.user.name] not in client.admins:
            await interaction.response.send_message("Only app admins can run this command", ephemeral=True)
        else:
            await interaction.response.send_message("Running task now", ephemeral=True)

            client.task_start = datetime.datetime.now()
            client.task_end = client.task_start + datetime.timedelta(minutes=1)
            #client.task_id = random.randint(0, 2)
            client.task_id = 0
            client.current_task = task_list.loc[client.task_id]
            if DEBUG: print(f"Task {client.task_id} was chosen")

            if client.current_task["Has File"]:
                for player in client.players:
                    player[1] = False
                    await player[0].send(
                        f"{client.current_task["Task Description"]} Respond <t:{round(client.task_end.timestamp())}:R>",
                        file=discord.File(str(BASE_DIR) + "/" + client.current_task["File Path"]))
                    if DEBUG: print(f"Sent to {player[0].name}")
            else:
                for player in client.players:
                    player[1] = False
                    await player[0].send(
                        f"{client.current_task["Task Description"]} Respond <t:{round(client.task_end.timestamp())}:R>")
                    if DEBUG: print(f"Sent to {player[0].name}")

            await interaction.response.send_message("Tasks have been sent", ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.response.send_message("Task failed, please retry", ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.guild:
        if datetime.datetime.now() < client.task_end:
            if client.current_task["Answer"].lower() in message.content.lower():
                await message.channel.send("Correct")
                client.players = [[player[0], True] if player[0] == message.author else player for player in client.players]
            else:
                await message.channel.send("Incorrect")
        else:
            await message.channel.send("The task has already ended")

#toggle random tasks

#help

@client.tree.command(name="view_players", description="Let admins view current player list")
async def view_players(interaction: discord.Interaction):
    if [interaction.user.id, interaction.user.name] in client.admins:
        await interaction.response.send_message(client.players, ephemeral=True)
    else:
        await interaction.response.send_message("Only app admins can run this command", ephemeral=True)

if __name__ == "__main__":
    client.run(TOKEN, log_handler=handler)
