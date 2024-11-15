#### #### Imports #### ####

import re, json, pathlib
from main import DuelComputer_Client
import discord
from discord.ext import commands
from discord import app_commands

#### #### Statics #### ####

enum_monster_properties = [
    None,
    {'en': 'Creator God', 'ja': '創造神族'},
    {'en': 'Special Summon Monster', 'ja': '特殊召喚', 'ko': '특수 소환'},
    {'de': 'Ungeheuer', 'en': 'Beast', 'es': 'Bestia', 'fr': 'Bête', 'it': 'Bestia', 'ja': '獣族', 'ko': '야수족',
     'pt': 'Besta'},
    {'de': 'Effekt', 'en': 'Effect', 'es': 'Efecto', 'fr': 'Effet', 'it': 'Effetto', 'ja': '効果', 'ko': '효과',
     'pt': 'Efeito'},
    {'de': 'Fisch', 'en': 'Fish', 'es': 'Pez', 'fr': 'Poisson', 'it': 'Pesce', 'ja': '魚族', 'ko': '어류족',
     'pt': 'Peixe'},
    {'de': 'Normale', 'en': 'Normal', 'es': 'Normal', 'fr': 'Normaux', 'it': 'Normale', 'ja': '通常', 'ko': '일반',
     'pt': 'Normal'},
    {'de': 'Flipp', 'en': 'Flip', 'es': 'Volteo', 'fr': 'Flip', 'it': 'Scoperta', 'ja': 'リバース', 'ko': '리버스',
     'pt': 'Virar'},
    {'de': 'Hexer', 'en': 'Spellcaster', 'es': 'Lanzador de Conjuros', 'fr': 'Magicien', 'it': 'Incantatore',
     'ja': '魔法使い族', 'ko': '마법사족', 'pt': 'Mago'},
    {'de': 'Maschine', 'en': 'Machine', 'es': 'Máquina', 'fr': 'Machine', 'it': 'Macchina', 'ja': '機械族',
     'ko': '기계족', 'pt': 'Machine'},
    {'de': 'Union', 'en': 'Union', 'es': 'Unión', 'fr': 'Union', 'it': 'Unione', 'ja': 'ユニオン', 'ko': '유니온',
     'pt': 'União'},
    {'de': 'Fusion', 'en': 'Fusion', 'es': 'Fusión', 'fr': 'Fusion', 'it': 'Fusione', 'ja': '融合', 'ko': '융합',
     'pt': 'Fusão'},
    {'de': 'Krieger', 'en': 'Warrior', 'es': 'Guerrero', 'fr': 'Guerrier', 'it': 'Guerriero', 'ja': '戦士族',
     'ko': '전사족', 'pt': 'Guerreiro'},
    {'de': 'Ungeheuer-Krieger', 'en': 'Beast-Warrior', 'es': 'Guerrero-Bestia', 'fr': 'Bête-Guerrier',
     'it': 'Guerriero-Bestia', 'ja': '獣戦士族', 'ko': '야수전사족', 'pt': 'Besta-Guerreira'},
    {'de': 'Unterweltler', 'en': 'Fiend', 'es': 'Demonio', 'fr': 'Démon', 'it': 'Demone', 'ja': '悪魔族',
     'ko': '악마족', 'pt': 'Demônio'},
    {'de': 'Fee', 'en': 'Fairy', 'es': 'Hada', 'fr': 'Elfe', 'it': 'Fata', 'ja': '天使族', 'ko': '천사족',
     'pt': 'Fada'},
    {'de': 'Pendel', 'en': 'Pendulum', 'es': 'Péndulo', 'fr': 'Pendule', 'it': 'Pendulum', 'ja': 'ペンデュラム',
     'ko': '펜듈럼', 'pt': 'Pêndulo'},
    {'de': 'Seeschlange', 'en': 'Sea Serpent', 'es': 'Serpiente Marina', 'fr': 'Serpent de Mer',
     'it': 'Serpente Marino', 'ja': '海竜族', 'ko': '해룡족', 'pt': 'Serpente Marinha'},
    {'de': 'Xyz', 'en': 'Xyz', 'es': 'Xyz', 'fr': 'Xyz', 'it': 'Xyz', 'ja': 'エクシーズ', 'ko': '엑시즈', 'pt': 'Xyz'},
    {'de': 'Synchro', 'en': 'Synchro', 'es': 'Sincronía', 'fr': 'Synchro', 'it': 'Synchro', 'ja': 'シンクロ',
     'ko': '싱크로', 'pt': 'Sincro'},
    {'de': 'Empfänger', 'en': 'Tuner', 'es': 'Cantante', 'fr': 'Syntoniseur', 'it': 'Tuner', 'ja': 'チューナー',
     'ko': '튜너', 'pt': 'Regulador'},
    {'de': 'Drache', 'en': 'Dragon', 'es': 'Dragón', 'fr': 'Dragon', 'it': 'Drago', 'ja': 'ドラゴン族', 'ko': '드래곤족',
     'pt': 'Dragão'},
    {'de': 'Wyrm', 'en': 'Wyrm', 'es': 'Wyrm', 'fr': 'Wyrm', 'it': 'Wyrm', 'ja': '幻竜族', 'ko': '환룡족',
     'pt': 'Wyrm'},
    {'de': 'Link', 'en': 'Link', 'es': 'Enlace', 'fr': 'Lien', 'it': 'Link', 'ja': 'リンク', 'ko': '링크', 'pt': 'Link'},
    {'de': 'Fels', 'en': 'Rock', 'es': 'Roca', 'fr': 'Rocher', 'it': 'Roccia', 'ja': '岩石族', 'ko': '암석족',
     'pt': 'Rocha'},
    {'de': 'Pflanze', 'en': 'Plant', 'es': 'Planta', 'fr': 'Plante', 'it': 'Pianta', 'ja': '植物族', 'ko': '식물족',
     'pt': 'Planta'},
    {'de': 'Spirit', 'en': 'Spirit', 'es': 'Spirit', 'fr': 'Spirit', 'it': 'Spirit', 'ja': 'スピリット', 'ko': '스피릿',
     'pt': 'Espírito'},
    {'de': 'Ritual', 'en': 'Ritual', 'es': 'Ritual', 'fr': 'Rituel', 'it': 'Rituale', 'ja': '儀式', 'ko': '의식',
     'pt': 'Ritual'},
    {'de': 'Zwilling', 'en': 'Gemini', 'es': 'Géminis', 'fr': 'Gémeau', 'it': 'Gemello', 'ja': 'デュアル', 'ko': '듀얼',
     'pt': 'Gêmeos'},
    {'de': 'Reptil', 'en': 'Reptile', 'es': 'Reptil', 'fr': 'Reptile', 'it': 'Rettile', 'ja': '爬虫類族',
     'ko': '파충류족', 'pt': 'Réptil'},
    {'de': 'Cyberse', 'en': 'Cyberse', 'es': 'Ciberso', 'fr': 'Cyberse', 'it': 'Cyberse', 'ja': 'サイバース族',
     'ko': '사이버스족', 'pt': 'Ciberso'},
    {'de': 'Aqua', 'en': 'Aqua', 'es': 'Aqua', 'fr': 'Aqua', 'it': 'Acqua', 'ja': '水族', 'ko': '물족', 'pt': 'Aqua'},
    {'de': 'Zombie', 'en': 'Zombie', 'es': 'Zombi', 'fr': 'Zombie', 'it': 'Zombie', 'ja': 'アンデット族', 'ko': '언데드족',
     'pt': 'Zumbi'},
    {'de': 'Psi', 'en': 'Psychic', 'es': 'Psíquico', 'fr': 'Psychique', 'it': 'Psichico', 'ja': 'サイキック族',
     'ko': '사이킥족', 'pt': 'Psíquico'},
    {'de': 'Insekt', 'en': 'Insect', 'es': 'Insecto', 'fr': 'Insecte', 'it': 'Insetto', 'ja': '昆虫族', 'ko': '곤충족',
     'pt': 'Inseto'},
    {'de': 'Geflügeltes Ungeheuer', 'en': 'Winged Beast', 'es': 'Bestia Alada', 'fr': 'Bête Ailée',
     'it': 'Bestia Alata', 'ja': '鳥獣族', 'ko': '비행야수족', 'pt': 'Besta Alada'},
    {'de': 'Dinosaurier', 'en': 'Dinosaur', 'es': 'Dinosaurio', 'fr': 'Dinosaure', 'it': 'Dinosauro',
     'ja': '恐竜族', 'ko': '공룡족', 'pt': 'Dinossauro'},
    {'de': 'Pyro', 'en': 'Pyro', 'es': 'Piro', 'fr': 'Pyro', 'it': 'Pyro', 'ja': '炎族', 'ko': '화염족', 'pt': 'Piro'},
    {'de': 'Donner', 'en': 'Thunder', 'es': 'Trueno', 'fr': 'Tonnerre', 'it': 'Tuono', 'ja': '雷族', 'ko': '번개족',
     'pt': 'Trovão'},
    {'de': 'Göttliches Ungeheuer', 'en': 'Divine-Beast', 'es': 'Bestia Divina', 'fr': 'Bête Divine',
     'it': 'Divinità-Bestia', 'ja': '幻神獣族', 'ko': '환신야수족', 'pt': 'Besta Divina'},
    {'de': 'Toon', 'en': 'Toon', 'es': 'Toon', 'fr': 'Toon', 'it': 'Toon', 'ja': 'トゥーン', 'ko': '툰', 'pt': 'Toon'}
]

enum_linkArrow = [
    'unused',
    ':arrow_lower_left:',
    ':arrow_down:',
    ':arrow_lower_right:',
    ':arrow_left:',
    'unused',
    ':arrow_right:',
    ':arrow_upper_left:',
    ':arrow_up:',
    ':arrow_upper_right:']

#### #### Class #### ####


class Cog_YGORGDB(commands.Cog):

    #### #### Attributes #### ####

    ygorgdbcache_file_path = pathlib.Path(__file__).parent.parent / 'resources//ygorgdb_cache.json'

    bot_client: DuelComputer_Client
    ygorgdb_cache = {  # Default cache file template
        'X-Cache-Revision': 0,
        'cache_qna': {},
        'cache_card': {},
    }

    #### #### Structors #### ####

    def __init__(self, bot_client: DuelComputer_Client) -> None:
        self.bot_client = bot_client

        # If there is no cache, then create one using the default format ygorgdb_cache
        if not self.ygorgdbcache_file_path.is_file():  # If there is no config file...
            with open(
                    file=self.ygorgdbcache_file_path,
                    mode='w+',
                    encoding='utf8'
            ) as cache_file:  # Create one
                json.dump(self.ygorgdb_cache, cache_file, sort_keys=True, indent=4)

        else:  # Otherwise load the config from the existing file
            with open(
                    file=self.ygorgdbcache_file_path,
                    mode='r+',
                    encoding='utf8'
            ) as cache_file:
                self.ygorgdb_cache = json.load(cache_file)

        # Load the context menu commands
        self.list_of_context_menu_commands_to_add = [
            app_commands.ContextMenu(name='Read Database Q&A Link', callback=self.read_qa_link),
        ]
        for context_menu_command in self.list_of_context_menu_commands_to_add:
            self.bot_client.tree.add_command(context_menu_command)

        return

    def __del__(self) -> None:
        # Write the cache to the json file.
        with open(self.ygorgdbcache_file_path, 'r+', encoding='utf8') as cache_file:
            json.dump(self.ygorgdb_cache, cache_file, sort_keys=True, indent=4)
        return

    async def cog_unload(self) -> None:
        for context_menu_command in self.list_of_context_menu_commands_to_add:
            self.bot_client.tree.remove_command(context_menu_command.name, type=context_menu_command.type)
        return

    #### #### Slash Commands #### ####

    @app_commands.command(name='card_display')
    @app_commands.describe(card_id='Card ID to query and display')
    async def display_card_by_id(self, interaction: discord.Interaction, card_id: str):
        await interaction.response.defer(thinking=False) # Getting the card data will probably take >3s
        data_of_card_to_display = await self.get_card_data(card_id)
        embed_of_card_to_be_sent = await self.build_card_embed(data_of_card_to_display)
        await interaction.followup.send(embed=embed_of_card_to_be_sent)

    #### #### App Commands #### #### Make sure to add these to the constructor!

    async def read_qa_link(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer(thinking=False) # This could take longer than 3s.

        # Get the QA IDs via regex
        id_of_qa_posts_in_message = re.search(r'db.ygoresources.com/qa#(\d*)', message.content)
        if id_of_qa_posts_in_message is None:
            await interaction.followup.send('Could not locate the Q&A id(s).')
            return

        # For each of the QAs found replace the card ids with the names (save the ids for the dropdown!)
        list_of_embeds_for_QAs_in_message = []
        list_of_card_IDs_in_all_QAs = []
        for QA_IDs_found_in_message in id_of_qa_posts_in_message.groups():

            # Create a new embed and add it to the list of embeds to display
            embed_for_this_QA = discord.Embed()
            list_of_embeds_for_QAs_in_message.append(embed_for_this_QA)

            # Get the required data, loading from the cache if possible, saving to the cache if not.
            data_for_this_QA = await self.get_qa_data(QA_IDs_found_in_message)
            list_of_card_IDs_in_all_QAs = [
                await self.get_card_data(str(card_id)) for card_id in data_for_this_QA['cards']
            ]

            # Use english if possible, otherwise use japanese.
            locale = 'en'
            if 'en' not in data_for_this_QA['qaData']: locale = 'ja'
            localized_QA_data = data_for_this_QA['qaData'][locale]

            # Replace the <<ids>> with the card names.
            for qa_data_component in localized_QA_data: # For each part of the Q&A
                if isinstance(localized_QA_data[qa_data_component], str): # If the part is a string...
                    for qa_card in list_of_card_IDs_in_all_QAs: # Take each card
                        localized_QA_data[qa_data_component] = localized_QA_data[qa_data_component].replace(
                            # And replace its id with its name.
                            f'<<{qa_card["cardData"][locale]["id"]}>>',
                            f'***{qa_card["cardData"][locale]["name"]}***'
                        )

            # Now construct the embed! Split the question and answer if they're too long.
            embed_char_limit = 1024

            # Question
            qa_question_text = localized_QA_data['question']
            qa_question_segments = [
                qa_question_text[i:i+embed_char_limit] for i in range(0, len(qa_question_text), embed_char_limit)
            ]
            embed_for_this_QA.add_field( # Initial field
                name='Question',
                value=qa_question_segments[0]
            )
            for question_segment in qa_question_segments[1:]: # (cont.) if necessary
                embed_for_this_QA.add_field(
                    name='Question (cont.)',
                    value=question_segment
                )

            # Answer
            qa_answer_text = localized_QA_data['answer']
            qa_answer_segments = [
                qa_answer_text[i:i + embed_char_limit] for i in range(0, len(qa_answer_text), embed_char_limit)
            ]
            embed_for_this_QA.add_field( # Initial field
                name='Answer',
                value=qa_answer_segments[0]
            )
            for answer_segment in qa_answer_segments[1:]:  # (cont.) if necessary
                embed_for_this_QA.add_field(
                    name='Answer (cont.)',
                    value=answer_segment
                )

        # Send all the embeds, and let people select the cards from a dropdown!
        await interaction.followup.send(
            embeds=list_of_embeds_for_QAs_in_message, # this is all the QAs
            view=View_QADropdown(list_of_card_IDs_in_all_QAs, cog_instance=self)
        )

    #### #### Methods #### ####

    async def get_card_data(self, card_id: str) -> dict:
        # If the card id is not in the cache, add it to the cache.
        if card_id not in list(self.ygorgdb_cache['cache_card'].keys()):

            # First open the api post request and get the information.
            async with self.bot_client.api_client.get(
                url=r'https://db.ygoresources.com/data/card/' + card_id
            ) as request_response:
                if request_response.status != 200:
                    raise Exception(f'Card retrieval failed: <{request_response.status}>\n{request_response.url}')

                # Check the revision header
                received_x_cache_revision = int(request_response.headers.get('X-Cache-Revision'))
                if received_x_cache_revision > self.ygorgdb_cache['X-Cache-Revision']:
                    await self.manifest_revision(received_x_cache_revision)

                # If the request was successful, save the response json to the cache as an entry.
                self.ygorgdb_cache['cache_card'][card_id] = await request_response.json()

        # After updating the cache (if necessary), we can return the Q&A from the cache.
        return self.ygorgdb_cache['cache_card'][card_id]

    async def get_qa_data(self, qa_id: str) -> dict:
        # If the qna id is not in the cache, add it to the cache.
        if qa_id not in list(self.ygorgdb_cache['cache_qna'].keys()):

            # First open the api post request and get the information.
            async with self.bot_client.api_client.get(
                    url=r'https://db.ygoresources.com/data/qa/' + qa_id) as request_response:
                if request_response.status != 200:
                    raise Exception(f'Q&A retrieval failed: <{request_response.status}>\n{request_response.url}')

                # Check the revision header
                received_x_cache_revision = int(request_response.headers.get('X-Cache-Revision'))
                if received_x_cache_revision > self.ygorgdb_cache['X-Cache-Revision']:
                    await self.manifest_revision(received_x_cache_revision)

                # If the request was successful, save the response json to the cache as an entry.
                self.ygorgdb_cache['cache_qna'][qa_id] = await request_response.json()

        # After updating the cache, we can return the Q&A from the cache.
        return self.ygorgdb_cache['cache_qna'][qa_id]

    async def get_card_image_url(self, card_id: str) -> dict:

        # Get the manifest file from which we will extract the url of the image we need.
        card_artwork_manifest = await self.bot_client.api_request(
            url=r'https://artworks.ygoresources.com/manifest.json',
            method='GET'
        )

        # Pull out the json and select the bestArt of the card with the id we need.
        target_card_image_url = card_artwork_manifest['cards'][card_id]['1']['bestArt']

        if r'https:' not in target_card_image_url:
            target_card_image_url = f'https:{target_card_image_url}'
        return target_card_image_url

    async def build_card_embed(self, card_data: dict) -> discord.Embed:
        localized_card_data = card_data['cardData']['en' if 'en' in card_data['cardData'] else 'ja']

        # Build the embed
        card_embed = discord.Embed(
            title=localized_card_data['name'],
            url=r'https://db.ygoresources.com/card#' + str(localized_card_data['id']),
            description=''
        )

        # Add the image via the ygorg artwork db url
        thumbnail_url = await self.get_card_image_url(str(localized_card_data['id']))
        card_embed.set_thumbnail(url=thumbnail_url)

        # Parse the properties for Spells and Traps, i.e. Continuous, Quick-Play, etc.
        if localized_card_data['cardType'] != 'monster':
            if 'property' not in localized_card_data:
                card_embed.description += 'Normal'
            else:
                card_embed.description += localized_card_data['property'].title()
            card_embed.description += f" {localized_card_data['cardType']}".title()
            card_embed.add_field(
                name='Effect Text',
                value=localized_card_data['effectText'])

        else:  # Build it as a monster. Consider pendulum/xyz/link/normal

            # Level/Rank/Link/Scale
            card_embed.description = ''

            if 'level' in localized_card_data:
                card_embed.description += f"☆Level: {localized_card_data['level']}"

            elif 'rank' in localized_card_data:
                card_embed.description += f"★Rank: {localized_card_data['rank']}"

            elif 'linkRating' in localized_card_data:
                card_embed.description += f"Rating: Link-{localized_card_data['linkRating']}\t("

                for link_arrow in localized_card_data['linkArrows']:
                    card_embed.description += enum_linkArrow[int(link_arrow)]
                card_embed.description += ')'

            if 'pendulumScale' in localized_card_data:
                card_embed.description += f" | ⬖Pendulum Scale: {localized_card_data['pendulumScale']}"

            # Attribute
            card_embed.description += f"\n{localized_card_data['attribute'].upper()} - Attribute"

            # Properties, i.e. 'Normal', 'Tuner', 'Beast-Warrior', etc.
            property_string = list(map(  # Map them from the property enum.
                lambda prop: enum_monster_properties[prop]['en' if 'en' in card_data['cardData'] else 'ja'],
                localized_card_data['properties']
            ))
            card_embed.description += f"\n[{' / '.join(property_string)}]\n"

            # ATK/DEF
            card_embed.description += f"ATK: {localized_card_data['atk']}"
            if 'def' in localized_card_data: card_embed.description += f"\tDEF: {localized_card_data['def']}"

            # Pendulum Effect
            if 'pendulumEffectText' in localized_card_data:
                card_embed.add_field(
                    name='Pendulum Text',
                    value=localized_card_data['pendulumEffectText'])

            # Effect/Flavor Text
            card_embed.add_field(
                name='Card Text',
                value=localized_card_data['effectText'])

        return card_embed

    async def manifest_revision(self, latest_x_cache_revision) -> None:

        cache_changes = await self.bot_client.api_request(
            url=r'https://db.ygoresources.com/manifest/' + str(self.ygorgdb_cache['X-Cache-Revision']),
            method='GET'
        )

        print(f'Cache Changes:\n{cache_changes}')

        # Remove the old entries
        change_counter = [0, 0]
        if 'card' in cache_changes['data']:
            for card_id in cache_changes['data']['card']:
                if card_id in self.ygorgdb_cache['cache_card']:
                    self.ygorgdb_cache['cache_card'].pop(card_id)
                    change_counter[0] += 1

        if 'qa' in cache_changes['data']:
            for qa_id in cache_changes['data']['qa']:
                if qa_id in self.ygorgdb_cache['cache_qna']:
                    self.ygorgdb_cache['cache_qna'].pop(qa_id)
                    change_counter[1] += 1

        # Update the manifest revision and re-write the cache file.
        print(f'Invalidated {change_counter[0]} card entries and {change_counter[1]} QA entries.')
        self.ygorgdb_cache['X-Cache-Revision'] = latest_x_cache_revision
        return


#### #### Views #### ####

class View_QADropdown(discord.ui.View):
    def __init__(self, card_list, cog_instance: Cog_YGORGDB, *, locale='en', timeout=180) -> None:
        super().__init__(timeout=timeout)
        self.add_item(Select_QADropdown(card_list, cog_instance=cog_instance, locale=locale))
        return


class Select_QADropdown(discord.ui.Select):
    def __init__(self, card_list, cog_instance: Cog_YGORGDB, locale='en') -> None:
        self.cog_instance = cog_instance

        card_options = [discord.SelectOption(
            label=card['cardData'][locale if locale in card['cardData'] else 'ja']['name'],
            value=card['cardData'][locale if locale in card['cardData'] else 'ja']['id']
        ) for card in card_list]

        super().__init__(
            placeholder='Select cards to display from the Q&A entry.',
            options=card_options[:24]  # Make sure you don't put more options than is allowed! First 24 only.
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)  # This could take longer than 3s.
        selected_dropdown_card_data = await self.cog_instance.get_card_data(self.values[0])
        selected_dropdown_card_embed = await self.cog_instance.build_card_embed(selected_dropdown_card_data)
        await interaction.followup.send(embed=selected_dropdown_card_embed)
        await interaction.edit_original_response(view=self.view)  # Redraws the dropdown to deselect the monster.


#### #### Setup #### ####


async def setup(bot_client: DuelComputer_Client) -> None:
    await bot_client.add_cog(Cog_YGORGDB(bot_client))

#### #### End of File #### ####
