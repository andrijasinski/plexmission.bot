# Plexmission bot

This Telegram bot is created to manage Transmission downloads, move content to Plex libraries and more for managing your media server.

## Setup

TLDR - clone this repo, create TG bot via BotFather, start the bot.

### Step by step

1. Create new TG bot via [BotFather](https://core.telegram.org/bots#creating-a-new-bot). **PS keep your bot token!**

2. Clone this repository to your media server. Requirements to your server:
   - Bash (not tested on Windows)
   - Python 3
   - Pip
   - Transmission (why would you want to run it otherwise?)

3. Export env variables with bot auth token, transmission auth credentials and comma-separated list of authorized users. You can use `/start` command of this bot to get know your user ID.

Use `install-and-start.sh` script. It will install all dependencies to virtual environment and run bot. I recomment to use [tmux](https://computingforgeeks.com/linux-tmux-cheat-sheet) to run in separate session. Example script:
```bash
#!/bin/sh

export BOT_AUTH="bot token from BotFather"
export TRANSMISSION_AUTH="transmission_login:transmission_password"
export AUTHORIZED_USERS="userid" # or userid1,userid2,userid3 for multiple users

tmux new-session -d -s tg_bot './install-and-start.sh'
```

### Configuration

Adjust paths in `config.py` file for your use case.

## Support

**PS** this Telegram bot is created for my use case.
In case of questions or problems, create issue in this repository or contact maintainer - [@andrijasinski](https://github.com/andrijasinski)
