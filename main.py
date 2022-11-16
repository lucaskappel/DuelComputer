import os, json, sys, re
from datetime import date

import discord
from discord.ext import commands

#### #### #### ####


class Bot_Client(commands.Bot):
    async def setup_hook(self):
        for filename in os.listdir("extensions"):
            if filename.endswith(".py"):
                await self.load_extension(f"extensions.{filename[:-3]}")

#### #### #### ####


def load_config():
    if not os.path.exists('config.json'):  # If there is no config file
        with open(r"config.json", 'w', encoding='utf8') as config_file:  # Create one
            bot_config = {
                "auth_token": "abcdefghijklmnopqrstuvwxyz.123456.7890-abcdefghijklmnopqrstuvwxyz1234567",
                "owner_id": "183033825108951041",
                "command_prefix": "+",
                "CHALLONGE_USERNAME": "none",
                "CHALLONGE_TOKEN": "none",
            }
            json.dump(bot_config, config_file)  # Set the config to the above template
            sys.exit()  # User will need to edit the config file and set all the necessary info.
    else:  # Otherwise
        with open(r"config.json", encoding='utf8') as config_file:  # open the existing config
            bot_config = json.load(config_file)  # Load the config's contents
            return bot_config


def run_bot():
    bot_config = load_config()
    bot_client = Bot_Client(
        command_prefix=bot_config["command_prefix"],
        intents=discord.Intents.all()
    )

    @bot_client.event
    async def on_error(event, *args):
        with open(f'logs/error_{date.today().strftime("%Y%m%d_%H%M%S")}.log', 'a') as error_file:
            error_file.write(f'{bot_client.user} : Unhandled exception\n{event}\n{args}\n')

    @bot_client.event # Sync command string, and insult handling
    async def on_message(message):
        if message.author.bot: return  # Bot should not respond to itself or other bots ;i
        if message.author.id == int(bot_config["owner_id"]) and 'sync command tree now' in message.content:
            await bot_client.tree.sync()
            await message.channel.send(f"Command sync status: Complete")

        # Greeting
        if re.compile(r"^(good (morning|day|afternoon|evening)|greetings|hello).{1,2}duel.?(bot|machine|comp)",
                      re.IGNORECASE).match(message.content):
            await message.channel.send(f'Greetings, {message.author.display_name}.')

        # Insult handling
        if re.compile(r".*suck.*duel.?(bot|mach|comp)",
                      re.IGNORECASE).match(message.content):
            await message.channel.send(f'An amusing attempt to hurt my algorithmic feelings, meatbag.')

        await bot_client.process_commands(message) # after conversations, pass the message to the command handler

    @bot_client.event
    async def on_ready(): print(f'System {bot_client.user} initialized. Beginning guild observation.')

    bot_client.run(bot_config["auth_token"])  # Run the bot.

    #### #### #### ####


if __name__ == "__main__": run_bot()
