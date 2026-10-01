# T3LOs
![Static Badge](https://img.shields.io/badge/Python-3.14-blue)
![GitHub License](https://img.shields.io/github/license/Rhyslan/T3LOs)
![GitHub Release](https://img.shields.io/github/v/release/Rhyslan/T3LOs)

A discord app game where players receive random tasks and have 1 minute to respond with the correct answer. A part of a code is provided for every correct response with a hidden secret if the players can find where to enter the code.

This game was created for the Swinburne University of Technology unit GAM30006 - Experimental Game Design based on the prompt "*1 minute of wonderment*". This game was worked on by a team of 5 students over a period of 2 weeks.

## Getting Started
### Requirements
- [Python 3.14](https://www.python.org/downloads/release/python-3147/)
- Admin access to a Discord server
- A Discord account

### Installation
1. Install Python 3.14
2. Clone the repository
3. (Optional) Create a python virtual environment
4. Install requirements with `pip install -r requirements`
5. Create a Discord bot
    1. Go to [Discord Devloper Portal](https://discord.com/developers/home)
    2. Create a new application
    3. Go to the `Bot` tab and enable the `Message Content Intent` under `Privileged Gateway Intents`
    4. Copy the bot token. <ins>***DO NOT SHARE THIS WITH ANYONE!***</ins>
    5. Go to the `OAuth2` tab
    6. Select the `bot` and `applications.commands` scopes
    7. Select the following Bot Permissions
        - `Send Messages`
        - `Manage Messages`
        - `Attach Files`
        - `Read Message History`
        - `Use Slash Commands`
    8. Copy the generate URL and invite the bot to your server
6. Run `main.py`
7. When prompted, enter the bot token and the server ID[^1] of the server you've invited it to
8. When prompted, enter your discord user ID[^1] and username to register as an admin

### Usage
After running and setting up the bot for the first time, select from the menu which option you'd like to use.
- `Run bot` will close the menu and run the main bot script until the program is terminated.
- `Add admin` can be used to register more admins for the bot.
- `Remove admin` can be used to remove an admin from the bot, but only if there is at least 2 admins registered.
- `Clear commands from all servers` is used to de-register all the commands from ever server the bot is in (use when removing the bot from servers).

#### Bot Commands
| Command         | Description                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `/join_game`    | Adds you to the game                                                                                                      |
| `/leave_game`   | Removes you from the game                                                                                                 |
| `/help`         | Displays a help message describing the game                                                                               |
| `/run_task`     | <ins>**Admins only**</ins>: sends out a task to all current players.                                                          |
| `/view_players` | <ins>**Admins only**</ins>: Displays a list of all the current players. <br> Currently doesn't work with large player counts. |

## Gameplay
When a task if run, every registered player is sent a DM by the bot containing a question and a remaining time. Players have the specified time to respond with the correct answer. When a correct answer is sent, the bot will respond with a success message. If the answer is incorrect, the bot will respond with a failure message. 

### Reward System
When a player correctly responds to a task, they receive a section of a code. Once they receive all the parts of the code (only indicated by receiving the same part twice in a row), they need to combine all the parts of a code, then use a base64 decoder to get the original phrase. Then, they need to access the context menu of the T3LOs bot (specifically from the bot's profile) and use the `Enter Code` command, following the bot's prompt with the decoded code. If the code is correct, the bot will DM the player the reward message.

[^1]: Enable developer mode in Discord settings to view these
