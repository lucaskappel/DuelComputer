#### #### Imports #### ####

import json, re, aiohttp, pathlib
from datetime import date

import discord
from discord.ext import commands

#### #### Statics #### ####

#### #### Class #### ####


class DuelComputer_Client(commands.Bot):

    #### #### Attributes #### ####

    configuration_file_path = pathlib.Path(__file__).parent / 'configuration_settings.json'

    api_client: aiohttp.ClientSession
    configuration_settings = {
        'auth_token': 'abcdefghijklmnopqrstuvwxyz.123456.7890-abcdefghijklmnopqrstuvwxyz1234567',
        'owner_id': '183033825108951041',
        'command_prefix': '+'
    }

    #### #### Structors #### ####

    def __init__(self) -> None:

        # We have to do an if/else because we can't open the file before checking if it's there :d
        if not self.configuration_file_path.is_file():  # If there is no config file...
            with open(
                    file=self.configuration_file_path,
                    mode='w+',
                    encoding='utf8'
            ) as configuration_file:  # Create one
                json.dump(self.configuration_settings, configuration_file, sort_keys=True, indent=4)
                return  # User will need to edit the config file and set all the necessary info.

        else:  # Otherwise
            with open(
                    file=self.configuration_file_path,
                    mode='r+',
                    encoding='utf8'
            ) as configuration_file:  # load the config from the existing file
                self.configuration_settings = json.load(configuration_file)

        super().__init__(
            command_prefix=self.configuration_settings['command_prefix'],
            intents=discord.Intents.default(),
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name='for dissidence.'
            )
        )
        return

    async def setup_hook(self):

        # Load all extensions/cogs
        extensions_folder = pathlib.Path(__file__).parent / 'extensions'
        for file_path in extensions_folder.iterdir():
            if file_path.suffix == '.py':
                await self.load_extension(f'extensions.{file_path.stem}')

        # Create the api client which will be used throughout the bot's runtime.
        self.api_client = aiohttp.ClientSession()

        return

    async def close(self) -> None:
        await self.api_client.close()
        await super().close()
        return

    #### #### Overrides #### ####

    async def on_error(self, event, *args):
        with open(f'logs/error_{date.today().strftime("%Y%m%d_%H%M%S")}.log', 'a') as error_file:
            error_file.write(f'{self.user} : Unhandled exception\n{event}\n{args}\n')

    async def on_message(self, message: discord.Message):
        if message.author.bot: return  # Bot should not respond to itself or other bots ;i

        command_was_called_by_owner = message.author.id == int(self.configuration_settings['owner_id'])
        if command_was_called_by_owner and 'sync command tree' in message.content:
            await self.tree.sync()
            await message.channel.send(f'Command sync complete!')

        # Greeting
        if re.compile(r'^(good (morning|day|afternoon|evening)|greetings|hello).{1,2}duel.?(bot|machine|comp)',
                      re.IGNORECASE).match(message.content):
            await message.channel.send(f'Greetings, {message.author.display_name}.')

        # Insult handling
        if re.compile(r'.*suck.*duel.?(bot|mach|comp)',
                      re.IGNORECASE).match(message.content):
            await message.channel.send(f'An amusing attempt to hurt my algorithmic feelings, meatbag.')
        return

    async def on_ready(self):
        print(f'System {self.user} initialized. Beginning guild observation.')

    #### #### Methods #### ####

    async def api_request(self, method: str, url: str, params=None):
        if params is None: params = {}

        if method == 'GET':
            request_response = await self.api_client.get(url=url, params=params)
        elif method == 'POST':
            request_response = await self.api_client.post(url=url, params=params)
        elif method == 'DELETE':
            request_response = await self.api_client.delete(url=url, params=params)
        elif method == 'PUT':
            request_response = await self.api_client.put(url=url, params=params)
        else:
            raise Exception('Invalid method. GET, POST, PUT, and DELETE are allowed.')

        if request_response.status != 200:
            print(f'Error: API call returned status <{request_response.status}>')

        if 'json' in request_response.content_type:
            return_request_response = await request_response.json()
        else:
            return_request_response = request_response.content

        request_response.close()
        return return_request_response

    #### #### End of Class #### ####


#### #### Setup #### ####

def run_bot():
    DuelComputer_client = DuelComputer_Client()
    DuelComputer_client.run(DuelComputer_client.configuration_settings['auth_token'])  # Run the bot.


if __name__ == '__main__': run_bot()
