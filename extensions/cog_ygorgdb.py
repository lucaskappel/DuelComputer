import aiohttp, re, os, json
import discord
from discord.ext import commands
from discord import app_commands


class Cog_YGORGDB(commands.Cog):
    """Resource cog handles commands involving writeups, links, and image resources """

    ygorgdb_cache = { # Default cache file template
        "X-Cache-Revision": 0,
        "cache_qna": {},
        "cache_card": {}
    }

    #### #### #### ####

    def __init__(self, bot_client: commands.Bot) -> None:
        self.bot_client = bot_client

        # If there is no cache, then create one using the default format above.
        if not os.path.exists(r'resources/ygorgdb_cache.json'):
            with open(r'resources/ygorgdb_cache.json', 'w', encoding='utf8') as cache_file:
                json.dump(self.ygorgdb_cache, cache_file)

        # Load the cache
        with open(r'resources/ygorgdb_cache.json', 'r', encoding='utf8') as cache_file:
            self.ygorgdb_cache = json.load(cache_file)

        # Load the context menus
        self.context_menu_list = [
            app_commands.ContextMenu(
                name='Read Database Q&A Link',
                callback=self.read_qa_link)
        ]
        for context_menu in self.context_menu_list: self.bot_client.tree.add_command(context_menu)
        return

    def __del__(self):
        # Write the cache to the json file.
        with open(r'resources/ygorgdb_cache.json', 'w', encoding='utf8') as cache_file:
            json.dump(self.ygorgdb_cache, cache_file)

    async def cog_unload(self) -> None:
        # Unload the context menus
        for context_menu in self.context_menu_list: self.bot_client.tree.remove_command(
            context_menu.name, type=context_menu.type
        )
        return

    #### #### #### ####

    #### #### #### ####
    
    async def read_qa_link(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer(thinking=False) # This could take longer than 3s.

        # Get the ids via regex
        id_of_qa_posts_in_message = re.search(r"db.ygorganization.com\/qa#(\d*)", message.content)
        if id_of_qa_posts_in_message is None:
            await interaction.followup.send("Could not locate the Q&A id(s).")
        else:
            embed_list = []
            for qa_id_string in id_of_qa_posts_in_message.groups():

                # Create a new embed and add it to the list of embeds to display
                qa_embed = discord.Embed()
                embed_list.append(qa_embed)

                # Get the required data, loading from the cache if possible, saving to the cache if not.
                qa_data = await self.get_qa_data(qa_id_string)
                qa_card_list = [await self.get_card_data(str(card_id)) for card_id in qa_data['cards']]

                # Use english if possible, otherwise use japanese.
                locale = 'en'
                if 'en' not in qa_data['qaData']: locale = 'ja'

                # Replace the <<ids>> with the card names.
                for qa_data_component in qa_data['qaData'][locale]: # For each part of the Q&A
                    if isinstance(qa_data['qaData'][locale][qa_data_component], str): # If the part is a string...
                        for qa_card in qa_card_list: # Take each card
                            qa_data['qaData'][locale][qa_data_component] = qa_data['qaData'][locale][qa_data_component]\
                                .replace( # And replace its id with its name.
                                f'<<{qa_card["cardData"][locale]["id"]}>>',
                                f'***{qa_card["cardData"][locale]["name"]}***'
                            )

                # Now construct the embed!
                qa_embed.title = qa_data['qaData'][locale]['title']
                qa_embed.add_field(
                    name='Question',
                    value=qa_data['qaData'][locale]['question']
                )
                qa_embed.add_field(
                    name='Answer',
                    value=qa_data['qaData'][locale]['answer']
                )

            # Send all the embeds!
            await interaction.followup.send(embeds=embed_list)

    #### #### #### ####

    async def get_qa_data(self, qa_id):

        # If the qna id is not in the cache, add it to the cache.
        if qa_id not in list(self.ygorgdb_cache['cache_qna'].keys()):

            # First open the api post request and get the information.
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(
                        url=r"https://db.ygorganization.com/data/qa/" + qa_id) as request_response:
                    if request_response.status != 200:
                        print(f"Q&A retrieval failed: <{request_response.status}>\n{request_response.url}")
                        return

                    # If the request was successful, save the response json to the cache as an entry.
                    self.ygorgdb_cache['cache_qna'][qa_id] = await request_response.json()

        # After updating the cache, we can return the Q&A from the cache.
        return self.ygorgdb_cache['cache_qna'][qa_id]

    async def get_card_data(self, card_id):

        # If the qna id is not in the cache, add it to the cache.
        if card_id not in list(self.ygorgdb_cache['cache_card'].keys()):

            # First open the api post request and get the information.
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(
                        url=r"https://db.ygorganization.com/data/card/" + card_id) as request_response:
                    if request_response.status != 200:
                        print(f"Card retrieval failed: <{request_response.status}>\n{request_response.url}")
                        return

                    # If the request was successful, save the response json to the cache as an entry.
                    self.ygorgdb_cache['cache_card'][card_id] = await request_response.json()

        # After updating the cache, we can return the Q&A from the cache.
        return self.ygorgdb_cache['cache_card'][card_id]

    async def manifest_revision_check(self, interaction: discord.Interaction): # TODO

        # check the revision id, if it's the most recent one, don't need to do anything
        #if ygorgdb_cache['X-Cache-Revision'] >= latest_manifest_revision: return

        # But if it *is* different, we need to remove the outdated information.

        # Get the json object of the changes.
        #cache_changes = {}
        async with aiohttp.ClientSession() as client_session:
            async with client_session.post(
                    url=r"https://db.ygorganization.com/manifest/" + self.ygorgdb_cache['X-Cache-Revision']
            ) as request_response:
                cache_changes = await request_response.json()

        print(cache_changes)

        # TODO remove old stuff

        # Update the manifest revision and re-write the cache file.
        #ygorgdb_cache['X-Cache-Revision'] = latest_manifest_revision
        return

    #### #### #### ####


async def setup(bot_client: commands.Bot) -> None:
    await bot_client.add_cog(Cog_YGORGDB(bot_client))
