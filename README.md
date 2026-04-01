# T3LOs
A discord app game where players recieve random tasks and have 1 minute to respond with the correct answer. A part of a code is provided for every correct response with a hidden secret if the players can find where to enter the code.
## Setup
### Requirements
- Python 3.14
- A Discord Developer account and application
### Install
- Run ``pip install requirements.txt`` to install the dependancies
- Create a file called ``secrets.py`` in the ``/src/data/`` folder and add the following to it:
  ```python
  TOKEN = "[Your discord bot token]"
  MY_GUILD = "[Server ID of your server]"
  ```
- Run the ``add_admin.py`` file and add your discord account as a game admin. ***IF AN ADMIN IS NOT ADDED, THE TASKS CAN'T BE RUN!***
- Add your bot to your server with the required permissions
- Run ``main.py``

## Commands
These slash commands are accessed in the server you add your bot and link the server ID to.
| Command | Description |
| --- | --- |
| ``/join_game`` | Adds you to the game |
| ``/leave_game`` | Removes you from the game |
| ``/run_task`` | Admins only: sends out a task to all current players. |
| ``/help`` | Displays a help message describing the game |
| ``/view_players`` | Admins only: Displays a list of all the current players. Currently doesn't work with large player counts. |

## Reward System
When a player correctly reponds to a task, they receive a section of a code. Once they receive all the parts of the code (only indicated by receiving the same part twice in a row), they need to combine all the parts of a code, then use a base64 decoder to get the original phrase. Then, they need to access the context menu of the T3LOs bot (specifically from the bot's profile) and use the ``Enter Code`` command, following the bot's prompt with the decoded code. If the code is correct, the bot will DM the player the reward message.