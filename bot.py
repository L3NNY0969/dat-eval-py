import discord
import os
import io
import traceback
import sys
import time
import datetime
import asyncio
import random
import aiohttp
import pip
import random
import textwrap
from contextlib import redirect_stdout
from discord.ext import commands
import json
bot = commands.Bot(command_prefix=commands.when_mentioned_or('e.'), owner_id=277981712989028353)


bot.remove_command("help")

def dev_check(id):
    with open('data/devs.json') as f:
        devs = json.load(f)
        if id in devs:
            return True
    return False


def cleanup_code(content):
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
      
    return content.strip('` \n')


@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    await bot.change_presence(game=discord.Game(name="using ?help!"))


@bot.command()
async def help(ctx):
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Bot Commands')
    em.description = "**Who am I? I am dat banana boi #1982's simple eval bot. I can help you run Python code.** \n <this> means that the argument is **optional**. \n [this] means that the argument is **required**."
    em.add_field(name='help', value='Shows the help message for this bot.')
    em.add_field(name='eval [code]', value='Runs Python code. Great for testing. Also the main purpose of this bot.')
    em.add_field(name='invite', value='Aye! Invite me to your server.')
    em.add_field(name='ping', value='PONG! Returns websocket latency.')
    await ctx.send(embed=em)

    

@bot.command(hidden=True, name='eval', aliases=['val'])
async def _eval(ctx, *, body: str):
    if "bot.ws.token" in body:
        return await ctx.send("I see you have tried to leak my token. Nice try, buddy. :rofl:")
    if "os.environ" in body:
        return await ctx.send("You can't access my config vars. Nice try, though.")
    lol = bot.get_channel(408030365773463562)
    await lol.send(f"**{ctx.message.author.name}** has run the code: \n\n```{body}```")        
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')  

          
@bot.command()
async def invite(ctx):
    await ctx.send("Aye! Lemme join that server: https://discordapp.com/oauth2/authorize?client_id=406882538116743168&scope=bot&permissions=8")
    
    
@bot.command()
async def ping(ctx):
    """Premium ping pong giving you a websocket latency."""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='PoIIIng! Your supersonic latency is:')
    em.description = f"{bot.latency * 1000:.4f} ms"
    em.set_footer(text="Psst...A heartbeat is 27 ms!")
    await ctx.send(embed=em)
    
    
if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))

    
    
