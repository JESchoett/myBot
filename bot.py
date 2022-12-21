import discord
import responses

import os
from dotenv import load_dotenv


# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('DISC_TOKEN')
    GUILD = os.getenv('DISC_GUILD')
    #https://discordpy.readthedocs.io/en/latest/intents.html?highlight=intents
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return
        print(message)

        # Get the data
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # ? send privat   $ send public
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True)
        elif user_message[0] == '$':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=False)
        else:
            print("no response will be send")

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)