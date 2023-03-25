import discord
import random
import os
from dotenv import load_dotenv #zum Aufruf der .env Datei
from discord.ext import commands
import argparse #für die argument Beschreibung der commands

#File Import
from momentum import Momentum
from help import MyHelp

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
JEbot.help_command = MyHelp()


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
@JEbot.command(name="hello", description='Begrüßt den User', brief='Begrüßt den User')
async def hello(ctx):
    """
    Begrüßt den User
    """
    await ctx.send('Hello there!')

#id
@JEbot.command(name="id", description='gibt deine Discord User-ID an', brief='gibt deine Discord User-ID an')
async def id(ctx):
    """
    gibt deine Discord User-ID an
    """
    await ctx.send(ctx.message.author.id)

#roll
@JEbot.command(name="roll", description='Rolle einen Würfel', brief='Rolle einen Würfel')
async def roll(ctx, dice='d6', amount=1, system=''):
    """
    Rolle einen Würfel

    Argumente (= default):
        - dice = d6 [wie viele Seiten soll der Würfel haben?]
        - amount = 1 [wie oft soll gewürfelt werden?]
        - system = "" [wird mit einem bestimmten System gespielt?]
                   "Scion"  [Scion: Erfolge werden nochmal gewürfelt und bei einem Botch wird Momentum hinzu gefügt]
    """

    rolling = []
    rollingVal = []
    success = 0
    if system.lower() == "scion":
        dice = 'd10'
        system == "scion"

    for wuerfel in range (0,amount) :
        roll = True
        while roll:
            diceVal = random.randint(1, int(dice[1:]))
            rollingVal.append(diceVal)
            rolling.append(f"Wurf {wuerfel+1}: {diceVal}")
            if diceVal == 10 and system.lower("scion"):
                roll = True
            else:
                roll = False

    botch = False
    if system == "scion":
        success = rollingVal.count(8) + rollingVal.count(9) + rollingVal.count(10)
        rolling.append(f"Erfolge: {success}")
        if success == 0 and 1 in rollingVal:
            rolling.append(f"WOOOP BOTCH Momentum +2")
            botch = True


    returnString = str(rolling)
    returnString = returnString.replace('[', '')
    returnString = returnString.replace(']', '')
    returnString = returnString.replace(',', '\n')
    returnString = returnString.replace("'", '')

    await ctx.send(returnString)
    if botch:
        await JEbot.get_command('momentum').invoke(ctx, "add", "2")

@JEbot.command(name="chtotxt", description='den Inhalt des Channels in eine TXT schreiben', brief='den Inhalt des Channels in eine TXT schreiben')
async def chtotxt(ctx, limit=10):
    """
    den Inhalt des Channels in eine TXT schreiben

    Argumente (= default):
        - limit = 10 [wie viele Nachrichten soll zurück gegangen werden?]

    """
    #https://stackoverflow.com/questions/63464013/discord-python-export-an-entire-chat-into-txt-file
    filename = f"{ctx.channel.name}.txt"
    with open(filename, "w") as file:
        async for msg in ctx.channel.history(limit):
            file.write(f"{msg.clean_content}\n")
    with open(filename, "r") as file:
        await ctx.send(file=discord.File(file, filename))
    os.remove(filename)



#momentum
thisSession = Momentum()
@JEbot.command(name="momentum", description='Scion Momentum System', brief='Scion Momentum')
async def momentum(ctx, momentumModus="show", amount=1):
    """
    Das Scion Momentum System
    In dem PnP Scion kann momentum für Würfe ausgegeben werden um eine neue Chance zu haben oder mehr Würfel zu verwenden.

    Argumente (= default):
        - momentumModus = "show" [Wie viel Momentum hat die Party]\n
                          "add"  [füge Momentum zum Counter hinzu]\n
                          "sub"  [ziehe Momentum vom Counter ab]\n

    """

    if momentumModus == "spend":
        returnStr = (f"euer ausgegeben Momentum {thisSession.spendMomentum}")
        await ctx.send(returnStr)
    if momentumModus == "add":
        thisSession.sessionMomentum += amount
    if momentumModus == "sub" and thisSession.sessionMomentum < amount:
        await ctx.send("ich kann nicht mehr Momentum abziehen als ihr habt")
    elif momentumModus == "sub" and thisSession.sessionMomentum >= amount:
        thisSession.sessionMomentum -= amount
        thisSession.spendMomentum += amount
    returnStr = (f"euer aktuelles Momentum {thisSession.sessionMomentum}")
    await ctx.send(returnStr)

#ping
@JEbot.command(name="ping", description='Zeigt den Ping des Bots', brief='Zeigt den Ping des Bots')
async def ping(ctx):
  """Returns the latency of the bot."""
  await ctx.send(f"Pong! {round(JEbot.latency * 1000)}ms")

JEbot.run(TOKEN)
