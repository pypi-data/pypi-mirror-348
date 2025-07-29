# dmodkit

[![PyPI version](https://img.shields.io/pypi/v/dmodkit)](https://pypi.org/project/dmodkit/)
[![Python version](https://img.shields.io/pypi/pyversions/dmodkit)](https://pypi.org/project/dmodkit/)
[![License](https://img.shields.io/github/license/mochathehuman/dmodkit)](https://github.com/mochathehuman/dmodkit/blob/main/LICENSE)

**dmodkit** is a fast, no-fluff Discord moderation toolkit for `discord.py` bots. Plug it in, load commands, and go.


## Install:
```bash
pip install dmodkit
```

## Features

- Slash commands for:
  - Kick / Ban
  - Warns & Strikes (auto-kick on 3rd)
  - Timeout Mute / Unmute
  - Message Purge
  - Channel Lock / Unlock
  - Slowmode control
  - Nickname changes
  - Snipe (last deleted message)
- Command logging
- Warning history saved to `warnings.log`

> [!IMPORTANT]
>
> This project requires the following packages:
>
> - [`discord.py`](https://pypi.org/project/discord.py/) (v2.0.0 or higher)
> - [`loggingutil`](https://github.com/mochathehuman/loggingutil) (v1.2.2 or higher)
>
> Install them using:
>
> `pip install discord.py loggingutil==1.2.2`

## Quickstart

```
import discord
from discord.ext import commands
from discord import app_commands
from dmodkit import Modkit

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

modkit = Modkit(client, tree)
modkit.load_all()

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

client.run("YOUR_TOKEN")
```

## Logs

- Warnings: `warnings.log`
- Commands: `modkit.log`
- Supports buffering, compression, and rotation

## Planned

- Context menu moderation
- AutoMod keyword filters
- Persistent user notes

## Permissions

Ensure your bot has:

- Kick Members
- Ban Members
- Moderate Members
- Manage Messages
- Manage Nicknames
- Manage Channels