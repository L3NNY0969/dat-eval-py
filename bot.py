import discord
import sys
import os
import io
import pip
import random
import aiohttp
import asyncio
from discord.ext import commands
import traceback
bot = commands.Bot(command_prefix=commands.when_mentioned_or('*'), owner_id=277981712989028353)


bot.remove_command("help")


def cleanup_code(content):
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
      
    return content.strip('` \n')

@bot.command()
async def help(self, ctx, cmd=None):
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Bot Commands')
    em.description = "**Who am I? I am dat banana boi #1982's simple eval bot. I can help you run Python code.**"
    em.add_field(name='help <category|command>', value='Shows the help message for this bot.')
