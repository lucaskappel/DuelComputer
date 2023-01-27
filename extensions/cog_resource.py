#### #### Imports #### ####

import json, pathlib
from main import DuelComputer_Client
import discord
from discord.ext import commands
from discord import app_commands


#### #### Class #### ####

class Cog_Resource(commands.Cog):
    """Resource cog handles commands involving writeups, links, and image resources """

    #### #### Attributes #### ####

    ygo_resource_list: dict
    ygo_resource_list_path = pathlib.Path(__file__).parent.parent / 'resources//ygo_resource_list.json'
    ygo_resource_images = pathlib.Path(__file__).parent.parent / 'resources//images'

    #### #### Structors #### ####

    def __init__(self, bot_client: commands.Bot) -> None:
        self.bot_client = bot_client

        with open(self.ygo_resource_list_path, encoding='utf8') as json_file:
            self.ygo_resource_list = json.load(json_file)

        return

    #### #### Slash Commands #### ####

    async def slash_resource_autocomplete(
            self, interaction: discord.Interaction, current: str,) -> list[app_commands.Choice]:
        resources = [r for r in self.ygo_resource_list]
        return [
            app_commands.Choice(name=resource, value=resource)
            for resource in resources if current.lower() in resource.lower()
        ]

    @app_commands.command(name="resource")
    @app_commands.describe(query='Resource name to query for.')
    @app_commands.autocomplete(query=slash_resource_autocomplete)
    async def slash_resource(self, interaction: discord.Interaction, query: str):
        # If an argument was provided, display it, depending on what kind it is.
        resource = self.ygo_resource_list[query]

        if resource['type'] == 'link':
            await interaction.response.send_message(embed=discord.Embed(
                title=query,
                description=resource['help'],
                url=resource['content']
            ))

        elif resource['type'] == 'writeup':  # writeups are full text
            await interaction.response.send_message(
                f"__**{query}**__\n{resource['content']}")

        elif resource['type'] == 'image':  # images send their image file.
            with open(resource['content'], 'rb') as image_resource:
                await interaction.response.send_message(file=discord.File(image_resource))


#### #### Setup #### ####

async def setup(bot_client: DuelComputer_Client) -> None:
    await bot_client.add_cog(Cog_Resource(bot_client))

#### #### End of File #### ####
