# Filename: main.py
# Author: Dylan
# Created: 14/03/2026
# Description: Main bot script

import csv
import datetime
import logging
import random
import re
from pathlib import Path

import discord
import joblib
from discord import app_commands

import data.message_segments as msg_seg
from data.secrets import TOKEN, MY_GUILD

BASE_DIR = Path(__file__).resolve().parent
DEBUG = True

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

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


intents = discord.Intents.default()
intents.message_content = True
tasks_file = open("data/tasks.csv")
csv_reader = csv.DictReader(tasks_file)
reward_code = "Reason to be"
encoded_code = "UmVhc29uIHRvIGJl"
client = Telos(intents=intents, task_list=list(csv_reader), code=reward_code, encoded_code=encoded_code)
tasks_file.close()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

@client.tree.command(name="join_game")
async def join_game(interaction: discord.Interaction):
    """
    Only add user as play if they aren't already
    """
    if not [x for x in client.players if x["user"] == interaction.user]:
        client.players.append({"user": interaction.user, "answered?": False, "code_part": 0})
        await interaction.response.send_message("""SLEEPER ENJOINED. AWAIT INSTRUCTION

-# Why is it we spend a third of our lives vulnerable, mimicking death? What function could it have served in the ancient past? Did some horror once stalk the dark, taking those who witnessed it?"""
                                                , ephemeral=True)
    else:
        await interaction.response.send_message("SLEEPER ALREADY ENJOINED. **PLEASE** AWAIT INSTRUCTION", ephemeral=True)

@client.tree.command(name="leave_game")
async def leave_game(interaction: discord.Interaction):
    """
    Only remove user from players if they aren't already
    """
    if [x for x in client.players if x["user"] == interaction.user]:
        client.players = [x for x in client.players if x["user"] != interaction.user]
        await interaction.response.send_message("""SLEEPER VITALS LOST. ERASING RECORD...
DONE.

-# Is it better to suffer in truth, or thrive in ignorance?"""
                                                , ephemeral=True)
    else:
        await interaction.response.send_message("SLEEPER NOT FOUND", ephemeral=True)

@client.tree.command(name="run_task", description="ADMIN ONLY")
async def run_task(interaction: discord.Interaction):
    """
    Select new random task and send to all players
    """
    if len(client.players) <= 0:
        await interaction.response.send_message("NO AGENTS FOUND", ephemeral=True)
        return

    try:
        # Only run if user is admin
        if [interaction.user.id, interaction.user.name] not in client.admins:
            await interaction.response.send_message("INSUFFICIENT PERMISSIONS. THIS ATTEMPT WILL BE REPORTED. FURTHER ATTEMPTS MAY RESULT IN ~~**[REDACTED]**~~", ephemeral=True)
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

            match client.current_task["Task Type"]:
                case "hid_img":
                    for player in client.players:
                        player["answered?"] = False
                        due_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                        await player["user"].send(
                            f"{msg_seg.hid_img_intro.replace("[time]", f"<t:{round(due_time.timestamp())}:R>")}",
                            file=discord.File(str(BASE_DIR) + "/" + client.current_task["File Path"]),
                            delete_after=60.0)
                case "triv":
                    for player in client.players:
                        player["answered?"] = False
                        due_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                        await player["user"].send(
                            f"{msg_seg.triv_intro.replace("[time]", f"<t:{round(due_time.timestamp())}:R>")
                                .replace("[question]", client.current_task["Task Question"])}",
                            delete_after=60.0)
                case "hid_snd":
                    for player in client.players:
                        player["answered?"] = False
                        due_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                        await player["user"].send(
                            f"{msg_seg.hid_snd_intro.replace("[time]", f"<t:{round(due_time.timestamp())}:R>")}",
                            file=discord.File(str(BASE_DIR) + "/" + client.current_task["File Path"]),
                            delete_after=60.0)
                case "mys":
                    print("not done yet")
                    for player in client.players:
                        player["answered?"] = False
                        due_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
                        await player["user"].send(
                            f"{msg_seg.mys_intro.replace("[time]", f"<t:{round(due_time.timestamp())}:R>")}",
                            file=discord.File(str(BASE_DIR) + "/" + client.current_task["File Path"]),
                            delete_after=60.0)

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
                if old_msg.content.startswith("---BEGIN TRANSMISSION---"):
                    if client.current_task["Answer"].lower() in message.content.lower():
                        resp = "Correct"
                        match client.current_task["Task Type"]:
                            case "hid_img":
                                resp = msg_seg.hid_img_corr
                            case "triv":
                                resp = msg_seg.triv_corr
                            case "hid_snd":
                                resp = msg_seg.hid_snd_corr
                            case "mys":
                                resp = msg_seg.mys_corr

                        resp = resp.replace("[muse]", random.choice(msg_seg.musings))
                        next_code_part = next(item for item in client.players if item["user"] == message.author)["code_part"]
                        if next_code_part > len(client.split_code) - 1:
                            next_code_part = len(client.split_code) - 1
                        resp = resp.replace("[index]", str(next_code_part) + ": ").replace("[code]", client.split_code[next_code_part])

                        await message.channel.send(resp, delete_after=3600.0)
                        client.players = [{"user": player["user"], "answered?": True, "code_part": player["code_part"] + 1}
                                          if player["user"] == message.author else player for player in client.players]
                    else:
                        resp = "Incorrect"
                        match client.current_task["Task Type"]:
                            case "hid_img":
                                resp = msg_seg.hid_img_incorr
                            case "triv":
                                resp = msg_seg.triv_incorr
                            case "hid_snd":
                                resp = msg_seg.hid_snd_incorr
                            case "mys":
                                resp = msg_seg.mys_incorr

                        resp = resp.replace("[muse]", "")
                        await message.channel.send(resp, delete_after=60.0)
    else:
        if client.awaiting_code:
            if message.content == client.code:
                await message.delete()
                await message.author.send(msg_seg.reward, delete_after=60.0, silent=True)
            client.awaiting_code = False

@client.tree.context_menu(name="Enter Code")
async def enter_code(interaction: discord.Interaction, member: discord.Member):
    if member.id == client.user.id:
        await interaction.response.send_message("ENTER CODE:", ephemeral=True)
        client.awaiting_code = True

@client.tree.command(name="help")
async def help_message(interaction: discord.Interaction):
    await interaction.response.send_message("This game requires players to respond to tasks within 1 minute of receiving them.\n" +
                                            "Use `/join_game` to register as a player, and `/leave_game` to withdraw.\n" +
                                            "Tasks may be sent at any time, so be ready.",
                                            ephemeral=True)

@client.tree.command(name="view_players", description="ADMINS ONLY")
async def view_players(interaction: discord.Interaction):
    if [interaction.user.id, interaction.user.name] in client.admins:
        await interaction.response.send_message(client.players, ephemeral=True)
    else:
        await interaction.response.send_message("INSUFFICIENT PERMISSIONS. THIS ATTEMPT WILL BE REPORTED. FURTHER ATTEMPTS MAY RESULT IN ~~**[REDACTED]**~~", ephemeral=True)

if __name__ == "__main__":
    client.run(TOKEN, log_handler=handler)
