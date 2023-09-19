import sys
import os

import openai
import discord

from discord.ext import commands

from src.cmds.ai.chatgpt import Ai
from src.cmds.automation.youtube import Youtube
from src.config import SecretVars

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

discord_token = SecretVars.BOT_TOKEN
openai.api_key = SecretVars.OPENAI_API_KEY

class Bot(commands.Bot):
    """
        Base of the bot
    """

    def __init__(self, 
                 command_prefix="$", 
                 intents=discord.Intents.all(),
                 discord_token=None,
                 ):
        super().__init__(command_prefix=command_prefix, 
                         intents=intents)
        self.discord_token = discord_token

    async def on_ready(self):
        print(f"Success: {self.user.name} is now online!")
        await self.add_cog(Ai(self))
        await self.add_cog(Youtube(self))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        await self.process_commands(message)

# Initiate bot
nahida = Bot(command_prefix="$")