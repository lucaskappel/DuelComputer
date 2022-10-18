import json
import discord
from discord.ext import commands
import challonge

class Cog_Tournament(commands.Cog):

    def __init__(self, bot_client):
        """_client is the discord.ext.commands.Bot object which acts as the interface to discord for the bot."""

        self.bot_client = bot_client
        with open(r"config.json", encoding='utf8') as json_file:
            self.bot_config = json.load(json_file)
        challonge.set_credentials(
            self.bot_config["CHALLONGE_USERNAME"],
            self.bot_config["CHALLONGE_TOKEN"]
        )

    @commands.group(
        name='tournament',
        aliases=['t'])
    async def tournament(self, command_context: commands.Context):
        if command_context.author.id != 183033825108951041: return # Only run if it's me >:L
        print(challonge.tournaments.index())


async def setup(bot_client: commands.Bot) -> None:
    await bot_client.add_cog(Cog_Tournament(bot_client))
