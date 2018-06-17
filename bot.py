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
bot = commands.Bot(command_prefix=commands.when_mentioned_or('py.'), owner_id=411683912729755649)
bot._last_result = None


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
    await bot.change_presence(activity=discord.Game(name="with python code | py.help"))
    
    
@bot.event
async def on_command(ctx):
    bot.commands_run += 1
    log = bot.get_channel(454048592974577664)
    em = discord.Embed(color=0xffffff, title="Eval Ran")
    em.add_field(name = "Author", value = ctx.message.author.name)
    em.add_field(name="Command Content", value=f"```{ctx.message.content}```")
    em.set_thumbnail(url=ctx.guild.icon_url)
    await log.send(embed=em)
    

@bot.command()
async def help(ctx):
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Bot Commands')
    em.description = "**Credits to dat banana boi#1982 for this bot.**"
    em.add_field(name='eval', value='Runs Python code')
    em.add_field(name='ping', value='Returns websocket latency.')
    await ctx.send(embed=em)

    

@bot.command(name='eval')
async def _eval(ctx, *, body: str):
    if "bot.ws.token" in body:
        return await ctx.send("I see you have tried to get my token. Nice try tho.")
    if "os.environ" in body:
        return await ctx.send("You can't access my config vars. Nice try, tho.")
    lol = bot.get_channel(454048592974577664)
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
async def ping(ctx):
    """Gives you the bot's websocket latency."""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='Pong!')
    em.description = f"{bot.latency * 1000:.4f} ms"
    em.set_footer(text="Psst...A heartbeat is 27 ms!")
    await ctx.send(embed=em)
    
    
if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))

    
    
