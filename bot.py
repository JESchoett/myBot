import discord
import random

import os
from dotenv import load_dotenv

from discord.ext import commands

import logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#get the Bot Token from a .env file
load_dotenv()
TOKEN = os.getenv('DISC_TOKEN')
GUILD = os.getenv('DISC_GUILD')

#https://discordpy.readthedocs.io/en/latest/intents.html?highlight=intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

default_prefixes = ['$']
JEbot = commands.Bot(command_prefix = default_prefixes, case_insensitive=True, intents=discord.Intents.all())

@JEbot.event
async def on_ready():
    print(f'{JEbot.user} is now running!')
    list = [
        'hacker man coding',
        'mindlessly scrolling reddit',
        'thinking about a girl',
        'at the gym'
    ]
    activity = discord.Game(name=random.choice(list))
    await JEbot.change_presence(status=discord.Status.online, activity=activity)

#hello
@JEbot.command(name="hello", description='greets you', brief='greets you')
async def hello(ctx):
    await ctx.send('Hello there!')

#id
@JEbot.command(name="id", description='gibt deine Discord User-ID an', brief='gibt deine Discord User-ID an')
async def id(ctx):
    await ctx.send(ctx.message.author.id)

#roll
@JEbot.command(name="roll", description='rolle einen Würfel', brief='rolle einen Würfel')
async def roll(ctx, dice='d6', amount=1):
    rolling = []

    for _ in range (0,amount) :
        rolling.append("you rolled a:" + str(random.randint(1, int(dice[1:]))))

    returnString = str(rolling)
    returnString = returnString.replace('[', '')
    returnString = returnString.replace(']', '')
    returnString = returnString.replace(',', '\n')
    returnString = returnString.replace("'", '')
    await ctx.send(returnString)

@JEbot.command(name="chtotxt", description='den Inhalt des Channels in eine TXT schreiben', brief='den Inhalt des Channels in eine TXT schreiben')
async def chtotxt(ctx):
    #https://stackoverflow.com/questions/63464013/discord-python-export-an-entire-chat-into-txt-file
    filename = f"{ctx.channel.name}.txt"
    with open(filename, "w") as file:
        async for msg in ctx.channel.history(limit=None):
            file.write(f"{msg.clean_content}\n")

JEbot.run(TOKEN)
