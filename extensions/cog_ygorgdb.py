import aiohttp, re, os, json
import discord
from discord.ext import commands
from discord import app_commands


class Cog_YGORGDB(commands.Cog):
    """Resource cog handles commands involving writeups, links, and image resources """

    enum_monster_properties = [
        None,
        {"en": "Creator God", "ja": "創造神族"},
        {"en": "Special Summon Monster", "ja": "特殊召喚", "ko": "특수 소환"},
        {"de": "Ungeheuer", "en": "Beast", "es": "Bestia", "fr": "Bête", "it": "Bestia", "ja": "獣族", "ko": "야수족",
         "pt": "Besta"},
        {"de": "Effekt", "en": "Effect", "es": "Efecto", "fr": "Effet", "it": "Effetto", "ja": "効果", "ko": "효과",
         "pt": "Efeito"},
        {"de": "Fisch", "en": "Fish", "es": "Pez", "fr": "Poisson", "it": "Pesce", "ja": "魚族", "ko": "어류족",
         "pt": "Peixe"},
        {"de": "Normale", "en": "Normal", "es": "Normal", "fr": "Normaux", "it": "Normale", "ja": "通常", "ko": "일반",
         "pt": "Normal"},
        {"de": "Flipp", "en": "Flip", "es": "Volteo", "fr": "Flip", "it": "Scoperta", "ja": "リバース", "ko": "리버스",
         "pt": "Virar"},
        {"de": "Hexer", "en": "Spellcaster", "es": "Lanzador de Conjuros", "fr": "Magicien", "it": "Incantatore",
         "ja": "魔法使い族", "ko": "마법사족", "pt": "Mago"},
        {"de": "Maschine", "en": "Machine", "es": "Máquina", "fr": "Machine", "it": "Macchina", "ja": "機械族",
         "ko": "기계족", "pt": "Machine"},
        {"de": "Union", "en": "Union", "es": "Unión", "fr": "Union", "it": "Unione", "ja": "ユニオン", "ko": "유니온",
         "pt": "União"},
        {"de": "Fusion", "en": "Fusion", "es": "Fusión", "fr": "Fusion", "it": "Fusione", "ja": "融合", "ko": "융합",
         "pt": "Fusão"},
        {"de": "Krieger", "en": "Warrior", "es": "Guerrero", "fr": "Guerrier", "it": "Guerriero", "ja": "戦士族",
         "ko": "전사족", "pt": "Guerreiro"},
        {"de": "Ungeheuer-Krieger", "en": "Beast-Warrior", "es": "Guerrero-Bestia", "fr": "Bête-Guerrier",
         "it": "Guerriero-Bestia", "ja": "獣戦士族", "ko": "야수전사족", "pt": "Besta-Guerreira"},
        {"de": "Unterweltler", "en": "Fiend", "es": "Demonio", "fr": "Démon", "it": "Demone", "ja": "悪魔族",
         "ko": "악마족", "pt": "Demônio"},
        {"de": "Fee", "en": "Fairy", "es": "Hada", "fr": "Elfe", "it": "Fata", "ja": "天使族", "ko": "천사족",
         "pt": "Fada"},
        {"de": "Pendel", "en": "Pendulum", "es": "Péndulo", "fr": "Pendule", "it": "Pendulum", "ja": "ペンデュラム",
         "ko": "펜듈럼", "pt": "Pêndulo"},
        {"de": "Seeschlange", "en": "Sea Serpent", "es": "Serpiente Marina", "fr": "Serpent de Mer",
         "it": "Serpente Marino", "ja": "海竜族", "ko": "해룡족", "pt": "Serpente Marinha"},
        {"de": "Xyz", "en": "Xyz", "es": "Xyz", "fr": "Xyz", "it": "Xyz", "ja": "エクシーズ", "ko": "엑시즈", "pt": "Xyz"},
        {"de": "Synchro", "en": "Synchro", "es": "Sincronía", "fr": "Synchro", "it": "Synchro", "ja": "シンクロ",
         "ko": "싱크로", "pt": "Sincro"},
        {"de": "Empfänger", "en": "Tuner", "es": "Cantante", "fr": "Syntoniseur", "it": "Tuner", "ja": "チューナー",
         "ko": "튜너", "pt": "Regulador"},
        {"de": "Drache", "en": "Dragon", "es": "Dragón", "fr": "Dragon", "it": "Drago", "ja": "ドラゴン族", "ko": "드래곤족",
         "pt": "Dragão"},
        {"de": "Wyrm", "en": "Wyrm", "es": "Wyrm", "fr": "Wyrm", "it": "Wyrm", "ja": "幻竜族", "ko": "환룡족",
         "pt": "Wyrm"},
        {"de": "Link", "en": "Link", "es": "Enlace", "fr": "Lien", "it": "Link", "ja": "リンク", "ko": "링크", "pt": "Link"},
        {"de": "Fels", "en": "Rock", "es": "Roca", "fr": "Rocher", "it": "Roccia", "ja": "岩石族", "ko": "암석족",
         "pt": "Rocha"},
        {"de": "Pflanze", "en": "Plant", "es": "Planta", "fr": "Plante", "it": "Pianta", "ja": "植物族", "ko": "식물족",
         "pt": "Planta"},
        {"de": "Spirit", "en": "Spirit", "es": "Spirit", "fr": "Spirit", "it": "Spirit", "ja": "スピリット", "ko": "스피릿",
         "pt": "Espírito"},
        {"de": "Ritual", "en": "Ritual", "es": "Ritual", "fr": "Rituel", "it": "Rituale", "ja": "儀式", "ko": "의식",
         "pt": "Ritual"},
        {"de": "Zwilling", "en": "Gemini", "es": "Géminis", "fr": "Gémeau", "it": "Gemello", "ja": "デュアル", "ko": "듀얼",
         "pt": "Gêmeos"},
        {"de": "Reptil", "en": "Reptile", "es": "Reptil", "fr": "Reptile", "it": "Rettile", "ja": "爬虫類族",
         "ko": "파충류족", "pt": "Réptil"},
        {"de": "Cyberse", "en": "Cyberse", "es": "Ciberso", "fr": "Cyberse", "it": "Cyberse", "ja": "サイバース族",
         "ko": "사이버스족", "pt": "Ciberso"},
        {"de": "Aqua", "en": "Aqua", "es": "Aqua", "fr": "Aqua", "it": "Acqua", "ja": "水族", "ko": "물족", "pt": "Aqua"},
        {"de": "Zombie", "en": "Zombie", "es": "Zombi", "fr": "Zombie", "it": "Zombie", "ja": "アンデット族", "ko": "언데드족",
         "pt": "Zumbi"},
        {"de": "Psi", "en": "Psychic", "es": "Psíquico", "fr": "Psychique", "it": "Psichico", "ja": "サイキック族",
         "ko": "사이킥족", "pt": "Psíquico"},
        {"de": "Insekt", "en": "Insect", "es": "Insecto", "fr": "Insecte", "it": "Insetto", "ja": "昆虫族", "ko": "곤충족",
         "pt": "Inseto"},
        {"de": "Geflügeltes Ungeheuer", "en": "Winged Beast", "es": "Bestia Alada", "fr": "Bête Ailée",
         "it": "Bestia Alata", "ja": "鳥獣族", "ko": "비행야수족", "pt": "Besta Alada"},
        {"de": "Dinosaurier", "en": "Dinosaur", "es": "Dinosaurio", "fr": "Dinosaure", "it": "Dinosauro",
         "ja": "恐竜族", "ko": "공룡족", "pt": "Dinossauro"},
        {"de": "Pyro", "en": "Pyro", "es": "Piro", "fr": "Pyro", "it": "Pyro", "ja": "炎族", "ko": "화염족", "pt": "Piro"},
        {"de": "Donner", "en": "Thunder", "es": "Trueno", "fr": "Tonnerre", "it": "Tuono", "ja": "雷族", "ko": "번개족",
         "pt": "Trovão"},
        {"de": "Göttliches Ungeheuer", "en": "Divine-Beast", "es": "Bestia Divina", "fr": "Bête Divine",
         "it": "Divinità-Bestia", "ja": "幻神獣族", "ko": "환신야수족", "pt": "Besta Divina"},
        {"de": "Toon", "en": "Toon", "es": "Toon", "fr": "Toon", "it": "Toon", "ja": "トゥーン", "ko": "툰", "pt": "Toon"}
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

    ygorgdb_cache = { # Default cache file template
        "X-Cache-Revision": 0,
        "cache_qna": {},
        "cache_card": {},
    }

    #### #### Structors #### ####

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

    #### #### Slash Commands #### ####

    async def test_card_display(self, interaction: discord.Interaction):
        pass

    #### #### App Commands #### ####

    async def read_qa_link(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer(thinking=False) # This could take longer than 3s.

        # Get the ids via regex
        id_of_qa_posts_in_message = re.search(r"db.ygorganization.com\/qa#(\d*)", message.content)
        if id_of_qa_posts_in_message is None:
            await interaction.followup.send("Could not locate the Q&A id(s).")
        else: # For each of the QAs found replace the card ids with the names:
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
                qa_embed.title = qa_data['qaData'][locale]['title'][:255]
                qa_embed.add_field(
                    name='Question',
                    value=qa_data['qaData'][locale]['question']
                )
                qa_embed.add_field(
                    name='Answer',
                    value=qa_data['qaData'][locale]['answer']
                )

            # TODO: Add buttons to easily pull the relevant cards up

            # Send all the embeds!
            await interaction.followup.send(embeds=embed_list)

    #### #### Helper Methods #### ####

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

    async def build_card_embed(self, card_id):
        card_data = await self.get_card_data(card_id)
        card_data_local = card_data["en" if "en" in card_data else "ja"]

        # Build the embed
        card_embed = discord.Embed(title=card_data_local["name"])

        if card_data_local["cardType"] != "monster":
            card_embed.description = f"{card_data_local['property']} {card_data_local['cardType']}".title()
            card_embed.add_field(
                name="Effect Text",
                value=card_data_local["effectText"])

        else: # Build it as a monster. Consider pendulum/xyz/link/normal

            # Level/Rank/Link/Scale
            card_embed.description = ""

            if "level" in card_data_local:
                card_embed.description += f"☆Level: {card_data_local['level']}"

            elif "rank" in card_data_local:
                card_embed.description += f"★Rank: {card_data_local['rank']}"

            elif "linkRating" in card_data_local:
                card_embed.description += f"Rating: Link-{card_data_local['linkRating']}\t("

                for link_arrow in card_data_local['linkArrows']:
                    card_embed.description += self.enum_linkArrow[int(link_arrow)]
                card_embed.description += ")"

            if "pendulumScale" in card_data_local:
                card_embed.description += f"| ⬖Pendulum Scale: {card_data_local['pendulumScale']}"

            # Properties
            property_string = list(map( # Map them from the property enum.
                lambda prop: self.enum_monster_properties[prop]["en" if "en" in card_data else "ja"],
                card_data_local['properties']
            ))
            card_embed.description += f"\n[{' / '.join(property_string)}]\n"

            # ATK/DEF
            card_embed.description += f"ATK: {card_data_local['atk']}"
            if 'def' in card_data_local: card_embed.description += f"ATK: {card_data_local['def']}"

            # Pendulum Effect
            if 'pendulumEffectText' in card_data_local:
                card_embed.add_field(
                    name="Pendulum Text",
                    value=card_data_local['pendulumEffectText'])

            # Effect/Flavor Text
            card_embed.add_field(
                name="Card Text",
                value=card_data_local['effectText'])

        return card_embed

    #### #### Other Methods #### ####

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
