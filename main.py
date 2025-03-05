"""
ToDo´s:
- Roll Botch should add 2 momentum
- add before to chtotxt
- add BS Block Counter
- clear text of emojies
- chtotxt datetime
- fix chtotxt
"""
import discord
import random
import os
from dotenv import load_dotenv #zum Aufruf der .env Datei
from discord.ext import commands
import argparse #für die argument Beschreibung der commands
import requests

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
        'am Schlafen',
        'es lebt',
        'label nach links verschieben',
        'SCHOKOBON',
        'JJJ-EF IS THE BEST'
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
async def roll(ctx, dice='d6', amount=1, dmg=0, attack=0):
    """
    Rolle einen Würfel

    Argumente (= default):
        - dice = d6 [wie viele Seiten soll der Würfel haben?]
        - amount = 1 [wie oft soll gewürfelt werden?]
    """
    rolling = []

    if "d" not in dice and dice.isnumeric:
        amount = int(dice)
        dice = "d6"

    def rollStr():
        returnString = str(rolling)
        returnString = returnString.replace('[', '')
        returnString = returnString.replace(']', '')
        returnString = returnString.replace(',', '\n')
        returnString = returnString.replace("'", '')
        return returnString

    if dice.find("d") != 0:
        attack = dmg
        dmg = amount
        amount = dice[:dice.find("d")]
        amount = int(amount)

        dice = dice[dice.find("d"):]

    rollingVal = []
    rollSum=0
    for i in range (0,amount) :
        if len(rollingVal) == 150:
            break
        diceVal = random.randint(1, int(dice[1:]))
        rollSum += diceVal
        rollingVal.append(diceVal)
        rolling.append(f"Wurf {len(rollingVal)}: {diceVal}")

    rolling.append(f"Alle Würfel: {rollSum}")
    rollSum += dmg
    rollSum += attack
    if dmg != 0 or attack != 0:
        rolling.append(f"+ DMG ({dmg}) + Attack ({attack}): {rollSum}")

    await ctx.send(rollStr())

#sum
@JEbot.command(name="sum", description='Summiert die gegebenen werte', brief='Summiert die gegebenen werte')
async def sum(ctx, *args):
    """
    Summiert die gegebenen werte
    """
    summe = 0
    for arg in args:
        summe += int(arg)

    await ctx.send(f"summe: {summe}")

@JEbot.command(name="chtotxt", description='den Inhalt des Channels in eine TXT schreiben', brief='den Inhalt des Channels in eine TXT schreiben')
async def chtotxt(ctx, limitT=10):
    """
    den Inhalt des Channels in eine TXT schreiben

    Argumente (= default):
        - limit = 10 [wie viele Nachrichten soll zurück gegangen werden?]

    """
    emojies = ['(⌐■_■)']
    #https://stackoverflow.com/questions/63464013/discord-python-export-an-entire-chat-into-txt-file
    filename = f"{ctx.channel.name}.txt"
    messages = [message async for message in ctx.history(limit=limitT)]
    with open(filename, "w") as file:
        async for msg in messages:
            #msg.replace(emojies, '')
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
    Wichtig ist hierbei erstmal mit "new" den Player Count zu initialisieriern

    Argumente (= default):
        - momentumModus = "show" [Wie viel Momentum hat die Party]\n
                          "new"  [Ändert die Variablen  Max Momentum und Player count]\n
                          "add"  [füge Momentum zum Counter hinzu]\n
                          "sub"  [ziehe Momentum vom Counter ab]\n
        - amount = 1 [Größe der Änderung]
    """

    if momentumModus == "new":
        thisSession.playerCount = amount
        thisSession.maxMomentum = thisSession.playerCount*2
        returnStr = (f"eure Spieleranzahl ist {thisSession.playerCount}")
    if momentumModus == "spend":
        returnStr = (f"euer ausgegeben Momentum {thisSession.spendMomentum}")
        await ctx.send(returnStr)
    if momentumModus == "add":
        if thisSession.sessionMomentum + amount > thisSession.maxMomentum:
            thisSession.sessionMomentum = thisSession.maxMomentum
        else:
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


#hisScore
@JEbot.command(name="hisScore", description='Berichtsheft History Score', brief='Berichtsheft History Score')
async def hisScore(ctx):
    """
    Berichtsheft History Score

    """
    schuelerScore = {}
    async for msg in ctx.channel.history():
        if msg.author.id not in schuelerScore:
            schuelerScore[msg.author.id] = 1
        else:
            schuelerScore[msg.author.id] = schuelerScore[msg.author.id] + 1

    returnString = str(schuelerScore)
    returnString = returnString.replace('{', '')
    returnString = returnString.replace('}', '')
    returnString = returnString.replace(',', '\n')
    await ctx.send(returnString)

#dad jokes
headers = {
	"X-RapidAPI-Key": "5e10bab5f9msh3ece857aa93db73p108517jsn735116d3629a",
	"X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
}

@JEbot.command(name="dad", description='Gibt einen Dad Joke', brief='Gibt einen Dad Joke')
async def dad(ctx):
    """Returns a dad joke."""
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    response = requests.get(url, headers=headers)
    joke = response.json()["body"][0]["setup"] + "\n\n" + response.json()["body"][0]["punchline"]
    await ctx.send(joke)

JEbot.run(TOKEN)