import json

import discord
from discord.ext import commands


class Cog_Configuration(commands.Cog):
    """Handles configuration settings like where the bot can post what.
    _client is the bot\'s client
    guild_configs is a dictionary, loaded/saved from guild_configs.json, which keep track of the config settings"""

    default_configuration = { # This is the template for the config objects written to guild_config.json
                '_guild_alias': '',
                'bot_channel': -1,
                'resource_channel': [],
                'welcome_channel': []
            }

    def __init__(self, _client):
        """_client is the discord.ext.commands.Bot object which acts as the interface to discord for the bot."""
        self._client = _client

        # Load the guild configurations from the json file
        with open(r"resources\guild_configs.json", encoding='utf8') as json_file:
            self.guild_configs = json.load(json_file)
        return

    def __del__(self):
        """When the bot shuts down, write the current configuration object to a json file.
        Overwrites the previous one to keep track of any changes made while running."""

        with open(r"resources\guild_configs.json", 'w', encoding='utf8') as json_file:
            json.dump(self.guild_configs, json_file, indent=1, sort_keys=True)
        return

    def initialize_guild_config(self, guild):
        """This is called when a guild does not have a config file but needs one.
        Have to do this weird fruit un-rollup thing [*dict.keys()] because dict.keys() is a naughty boy"""

        if str(guild.id) not in [*self.guild_configs.keys()]: # make sure the guild doesn't already have a config
            self.guild_configs[guild.id] = self.default_configuration
            self.guild_configs[guild.id]['_guild_alias'] = guild.name
        return

    def update_guild_config(self):
        """Debug method; use this to update the format of the configuration files."""
        for guild in self._client.guilds:
            self.guild_configs[str(guild.id)]['_guild_alias'] = guild.name
        return

    async def bot_log(self, context, message, delete_context_message=True):
        """Use this to keep stuff clean. Deletes the calling message, prints the desired text."""

        bot_channel = context.guild.get_channel(int(self.guild_configs[str(context.guild.id)]['bot_channel']))
        if bot_channel != -1:
            if isinstance(message, str): # If the message is a string, we can just print it
                await bot_channel.send(message)
            elif isinstance(message, discord.Embed): # if the message is an embed, use it (use this for images)
                await bot_channel.send(embed=message)
        if context is not None and delete_context_message: await context.message.delete() # delete the message if wanted
        return

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Whenever a new guild is joined, create a configuration for it."""
        self.initialize_guild_config(guild)

    @commands.group(
        name='config',
        aliases=['c'],
        help='Bot configuration tools.',
        invoke_without_command=True
    )
    @commands.has_guild_permissions(view_audit_log=True)
    async def config(self, command_context):
        help_embed = discord.Embed(
            title='[+c | +config] : Configuration Commands',
            description='List the commands available within the configuration cog.',
            color=discord.colour.Color.blue()
        )
        help_embed.add_field(
            name='+c [set | s]',
            value='Sets a configuration setting for this guild.'
        )
        help_embed.add_field(
            name='+c [get | g]',
            value='Gets a configuration setting for this guild.'
        )
        await self.bot_log(command_context, help_embed)
        return

    @config.command(
        name='set',
        aliases=['s'],
        help='Set a configuration setting for this guild.'
    )
    async def set(self, command_context, *args):

        # Check to see if the guild is in the list, initialize the config if not.
        if str(command_context.guild.id) not in [*self.guild_configs.keys()]:
            self.initialize_guild_config(command_context.guild)

        # If no parameters are provided, show what parameters are available to set
        if len(args) == 0:
            help_embed = discord.Embed(
                title='+c [set | s] <parameter> <value?>: Set Guild Configuration',
                description='Set a setting for this guild\'s configuration',
                color=discord.colour.Color.blue()
            )
            help_embed.add_field(
                name='bot_channel',
                value='Toggles this channel as the target for meta-information messages from the bot.',
            )
            help_embed.add_field(
                name='resource_channel',
                value='Toggles this channel as able to use resource [+r] commands. Call again to remove from the list.',
            )
            await self.bot_log(command_context, help_embed)
            return

        #Check to see if the guild is in the list, initialize the config if not.
        if str(command_context.guild.id) not in [*self.guild_configs.keys()]:
            self.initialize_guild_config(command_context.guild)

        if args[0] in ['_guild_alias']:
            await self.bot_log(command_context, f'Error: {args[0]} is not mutable.', False)
            return

        # Check to see if the configuration is allowable.
        if args[0] not in [*self.guild_configs[str(command_context.guild.id)].keys()]:
            await self.bot_log(command_context, f"Statement: ```{args[0]}``` is not a valid configuration parameter.")

        # If marking the bot channel
        elif args[0] == 'bot_channel':

            # If the channel id is the same as the current bot channel, then un-set the bot channel to none.
            if self.guild_configs[str(command_context.guild.id)][args[0]] == command_context.channel.id:
                self.guild_configs[str(command_context.guild.id)][args[0]] = -1
                await self.bot_log(command_context, f'{command_context.channel.name} rescinded as the bot channel.')

            # Otherwise overwrite the previous bot channel with the current one
            else:
                self.guild_configs[str(command_context.guild.id)][args[0]] = command_context.channel.id
                await self.bot_log(command_context, f'{command_context.channel.name} set as the bot channel.')

        # If marking resource channels
        elif args[0] == 'resource_channel':

            # If the current channel is already marked as such, un-mark it
            if command_context.channel.id in self.guild_configs[str(command_context.guild.id)][args[0]]:
                self.guild_configs[str(command_context.guild.id)][args[0]].remove(command_context.channel.id)
                await self.bot_log(command_context, f'{command_context.channel.name} removed from resource_channels')

            # Otherwise add it to the list of resource channels.
            else:
                self.guild_configs[str(command_context.guild.id)][args[0]].append(command_context.channel.id)
                await self.bot_log(command_context, f'{command_context.channel.name} added to resource_channels')
        return

    @config.command(
        name='get',
        aliases=['g'],
        help='Get a configuration setting for this guild.'
    )
    async def getconfig(self, command_context, *args):
        if len(args) == 0: # If no arguments are passed, print the full configuration
            help_embed = discord.Embed(
                title='+c [get : g] <parameter>',
                description='List the guild configuration for <parameter>',
                color=discord.colour.Color.blue()
            )
            for key in [*self.guild_configs[str(command_context.guild.id)].keys()]:
                if isinstance(self.guild_configs[str(command_context.guild.id)][key], list):
                    help_embed.add_field(
                        name=key,
                        value='\n'.join([
                            command_context.guild.get_channel(channel_id).name for
                            channel_id in
                            self.guild_configs[str(command_context.guild.id)][key]
                        ])
                    )
                else:
                    help_embed.add_field(
                        name=key,
                        value=command_context.guild.get_channel(
                            self.guild_configs[str(command_context.guild.id)][key]
                        ).name
                    )

            await self.bot_log(command_context, help_embed)
        else:

            # If the provided command argument is not one of the available configuration options (+c g arg0 arg1 arg2)
            if args[0] not in [*self.guild_configs[str(command_context.guild.id)].keys()]:
                await self.bot_log(
                    command_context,
                    f"Statement: ```{args[0]}``` is an invalid configuration parameter."
                )

            # if args[0] is in the available configs, then we can display it based on what kind of config it is
            else:

                # If the config option is a list, list all the things in it
                if isinstance(self.guild_configs[str(command_context.guild.id)][args[0]], list):
                    description = '\n'.join([
                        command_context.guild.get_channel(channel_id).name for
                        channel_id in
                        self.guild_configs[str(command_context.guild.id)][args[0]]
                    ])

                #If the config option is not a list, then just list the thing
                else:
                    description = command_context.guild.get_channel(
                        self.guild_configs[str(command_context.guild.id)][args[0]]
                    ).name

                # Once the description is made, can send the now-configured embed.
                await self.bot_log(command_context, discord.Embed(
                    title=args[0],
                    description=description,
                    color=discord.colour.Color.blue()
                ))
        return


async def setup(bot_client: commands.Bot) -> None:
    await bot_client.add_cog(Cog_Configuration(bot_client))
