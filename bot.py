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
        'at the gym',
        'EE ist der Beste',
        'BERND',
        'HD ne 4K',
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
async def roll(ctx, dice='d6', amount=1, system=' '):
    rolling = []
    rollingVal = []
    success = 0
    if system.lower() == "scion":
        dice = 'd10'

    for _ in range (0,amount) :
        roll = True
        while roll:
            diceVal = random.randint(1, int(dice[1:]))
            rollingVal.append(diceVal)
            rolling.append(f"you rolled a: {diceVal}")
            if diceVal == 10 and system.lower("scion"):
                roll = True
            else:
                roll = False

    if system.lower() == "scion":
        success = rollingVal.count(8) + rollingVal.count(9) + rollingVal.count(10)
        rolling.append(f"number of successes: {success}")
        if success == 0 and 1 in rollingVal:
            rolling.append(f"WOOOP BOTCH Momentum +2")

    rolling.append(f"you rolled: {len(rollingVal)} times")

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
    await ctx.send(file)

sessionMomentum = 0
spendMomentum = 0
#momentum
@JEbot.command(name="momentum", description='Scion Momentum', brief='Scion Momentum')
async def momentum(ctx, momentumModus="show", amount=1):
    global sessionMomentum
    global spendMomentum

    if momentumModus == "add":
        sessionMomentum += amount
    if momentumModus == "sub" and sessionMomentum < amount:
        await ctx.send("ich kann nicht mehr Momentum abziehen als ihr habt")
    elif momentumModus == "sub" and sessionMomentum >= amount:
        sessionMomentum -= amount
        spendMomentum += amount
    returnStr = (f"euer aktuelles Momentum {sessionMomentum}")
    await ctx.send(returnStr)



JEbot.run(TOKEN)
