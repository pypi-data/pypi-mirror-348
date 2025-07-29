import json
from types import NoneType

import discord
from discord.ext import commands
from CharmCord.functions.Events._options_ import options
from CharmCord.functions.Messages._btnOpts_ import interactions
from CharmCord.tools import FunctionHandler, find_bracket_pairs, no_arguments
from .CommandHandler import load_commands
from .Commands import Commands
from .SlashCommands import SlashCommands
from ..CharmErrorHandling import CharmCordError
from ..globeHandler import update_globals, get_globals

global bots


class CharmCord:

    def __init__(
            self,
            prefix,
            case_insensitive,
            intents,
            activity,
            load_command_dir,
    ):
        """
        This function initializes a bot with specified prefix, case sensitivity, intents, activity, and loads command files.
        It determines intents based on user input and creates bot instances with the specified parameters.
        Additionally, it loads command files and sets up a JSON file for storing variables if it doesn't exist.
        :param prefix:
        :param case_insensitive:
        :param intents:
        :param activity:
        :param load_command_dir:
        """

        global bots

        # Initialize Start class
        self.prefix = prefix
        self.case_insensitive = case_insensitive
        self.intented = intents
        self._help_command = None
        self._clients = ""
        self.intent = ""
        self._activity = activity
        self.all_variables = {}
        self.bot = None

        # Determine intents
        if "all" in self.intented:
            self.intent = discord.Intents.all()
        elif "default" in self.intented:
            self.intent = discord.Intents.default()
        else:
            self.intent = discord.Intents.default()

        # Enable specific intents
        if "message" in self.intented:
            self.intent.message_content = True
        if "members" in self.intented:
            self.intent.members = True
        if "presences" in self.intented:
            self.intent.presences = True

        # Create bot instances
        # if self._activity
        self._clients = commands.Bot(
            command_prefix=self.prefix,
            case_insensitive=self.case_insensitive,
            intents=self.intent,
            activity=self._activity,
            help_command=self._help_command,
        )
        bots, self.bot = self._clients, self._clients
        update_globals("bots", self.bot)

        try:
            load_commands(load_command_dir)
        except FileNotFoundError:
            pass

        try:
            with open("variables.json", "r") as var:
                pass
        except FileNotFoundError:
            with open("variables.json", "w") as var:
                go = {"STRD": True}
                json.dump(go, var)

    @staticmethod
    def run(token: str):
        bots.run(token)


    def variables(self, variables: dict):
        for key, value in variables.items():
            self.all_variables[key] = value
        all_vars = self.all_variables
        update_globals("all", all_vars)

    @staticmethod
    def interaction_code(id_name: str, code: str):
        if id_name in interactions:
            raise CharmCordError(f"Multiple interactions with same ID found! Please make sure all IDs are unique",
                                 f"Interaction: {id_name}")
        interactions[id_name] = code
        return

    @staticmethod
    def slash_command(name: str, description: str, code: str, args: list[dict] = None) -> None:
         
        """
        Creates an interaction command wth the Discord API

        :param name: The name of your interaction command
        :param code: The charmcord code for your command
        :param args: The arguments for your interaction
        :param description: The description for your interaction
        :return: None
        """
        sl = SlashCommands().slash_command
        sl(name=name, code=code, args=args, description=description.lower(), bot=bots)

    @staticmethod
    def command(name: str, code: str, aliases: list = None) -> None:
        """

        :param name: The name of your prefix command
        :param code: The charmcord code for your command
        :param aliases: Different names that can invoke the command
        :return: None
        """
        co = Commands().command
        if aliases is None:
            co(name=name, code=code, bot=bots)
        else:
            co(name=name, code=code, aliases=aliases, bot=bots)

    # EVENTS BELOW

    def on_reaction_add(self, code: str = None):
        @self.bot.event
        async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
            try:
                options["reactionAdded"]["name"] = reaction.emoji.name
                options["reactionAdded"]["id"] = reaction.emoji.id
            except AttributeError:
                options["reactionAdded"]["name"] = reaction.emoji  # May Remove
                options["reactionAdded"]["id"] = 0
            options["reactionAdded"]["bot_reacted"] = reaction.me
            options["reactionAdded"]["users_reacted"] = [user async for user in reaction.users()]
            options["reactionAdded"]["count"] = reaction.count
            options["reactionAdded"]["username"] = user.name
            options["reactionAdded"]["userid"] = user.id
            options["reactionAdded"]["msgid"] = reaction.message.id
            options["reactionAdded"]["msgauthorid"] = reaction.message.author.id
            options["reactionAdded"]["msgauthorname"] = reaction.message.author.name

            if code is not None:
                final_code = await no_arguments(code, TotalFuncs, None)
                await find_bracket_pairs(final_code, TotalFuncs, None)
            return

    def on_reaction_remove(self, code=None):
        @self.bot.event
        async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
            try:
                options["reactionRemoved"]["name"] = reaction.emoji.name
                options["reactionRemoved"]["id"] = reaction.emoji.id
            except AttributeError:
                options["reactionRemoved"]["name"] = reaction.emoji  # May Remove
                options["reactionRemoved"]["id"] = 0
            options["reactionRemoved"]["bot_reacted"] = reaction.me
            options["reactionRemoved"]["users_reacted"] = [user async for user in reaction.users()]
            options["reactionRemoved"]["count"] = reaction.count
            options["reactionRemoved"]["username"] = user.name
            options["reactionRemoved"]["userid"] = user.id
            options["reactionRemoved"]["msgid"] = reaction.message.id
            options["reactionRemoved"]["msgauthorid"] = reaction.message.author.id
            options["reactionRemoved"]["msgauthorname"] = reaction.message.author.name

            if code is not None:
                final_code = await no_arguments(code, TotalFuncs, None)
                await find_bracket_pairs(final_code, TotalFuncs, None)
            return

    def on_message(self, code=None):
        @self.bot.event
        async def on_message(msg: discord.Message):
            options['onMessage']['channelid'] = msg.channel.id
            options['onMessage']['guildid'] = msg.guild.id

            for attr in options['onMessage'].keys():
                options['onMessage'][attr] = msg.attr

    def on_member_join(self, code=None):
        @self.bot.event
        async def on_member_join(member: discord.Member):
            options["memberJoined"]["id"] = member.id
            options["memberJoined"]["guildid"] = member.guild.id

            if code is not None:
                final_code = await no_arguments(code, TotalFuncs, None)
                await find_bracket_pairs(final_code, TotalFuncs, None)
            return

    def on_channel_updated(self, code=None):
        @self.bot.event
        async def on_guild_channel_update(before: discord.TextChannel, after: discord.TextChannel):
            options["oldChannel"]["name"] = before.name
            options["oldChannel"]["id"] = before.id
            options["oldChannel"]["type"] = before.type
            options["oldChannel"]["category"] = before.category
            if not isinstance(before.category, NoneType):
                options["oldChannel"]["categoryid"] = before.category.id
            options["oldChannel"]["guild"] = before.guild.name
            options["oldChannel"]["guildid"] = before.guild.id
            options["oldChannel"]["nsfw"] = before.nsfw
            options["oldChannel"]["delay"] = before.slowmode_delay

            options["newChannel"]["name"] = after.name
            options["newChannel"]["id"] = after.id
            options["newChannel"]["type"] = after.type
            options["newChannel"]["category"] = after.category
            if not isinstance(after.category, NoneType):
                options["newChannel"]["categoryid"] = after.category.id
            options["newChannel"]["guild"] = after.guild.name
            options["newChannel"]["guildid"] = after.guild.id
            options["newChannel"]["nsfw"] = after.nsfw
            options["newChannel"]["delay"] = after.slowmode_delay


            #for i in options["oldChannel"].keys():
            #    options["oldChannel"][i] =
            #for i in options["newChannel"].keys():
            #    options["newChannel"][i] = after.i
            if code is not None:
                final_code = await no_arguments(code, TotalFuncs, None)
                await find_bracket_pairs(final_code, TotalFuncs, None)

    def on_channel_deleted(self, code=None):
        @self.bot.event
        async def on_guild_channel_delete(channel):
            options["deletedChannel"]["name"] = channel.name
            options["deletedChannel"]["id"] = channel.id
            options["deletedChannel"]["type"] = channel.type
            options["deletedChannel"]["category"] = channel.category
            options["deletedChannel"]["categoryid"] = channel.category_id
            options["deletedChannel"]["guild"] = channel.guild
            options["deletedChannel"]["nsfw"] = channel.nsfw
            options["deletedChannel"]["delay"] = channel.slowmode_delay
            options["deletedChannel"]["created"] = channel.created_at
            # more options coming
            if code is not None:
                final_code = await no_arguments(code, TotalFuncs, None)
                await find_bracket_pairs(final_code, TotalFuncs, None)

    def on_ready(self, code: str):
        @self.bot.event
        async def on_ready():
            from CharmCord.CharmErrorHandling import CharmCordErrors
            final_code = await no_arguments(code, TotalFuncs, None)
            await find_bracket_pairs(final_code, TotalFuncs, None)
            try:
                await self.bot.tree.sync()
            except Exception as e:
                print(e)
                CharmCordErrors("All slash commands need a description")

class Intents:


    def __init__(self):
        if "all" in self.intented:
            self.intent = discord.Intents.all()
        elif "default" in self.intented:
            self.intent = discord.Intents.default()
        else:
            self.intent = discord.Intents.default()


def charmclient(
        prefix: str,
        case_insensitive: bool = False,
        intents: str | list = "Default",
        activity: discord.Activity = None,
        load_command_dir="commands",
):
    """
    CharmCord Discord Client
    """
    # Global variables
    global bots
    global TotalFuncs

    # Initialize FunctionHandler and register functions
    functions = FunctionHandler()
    TotalFuncs = functions
    update_globals("total", functions)
    functions.register_functions()

    # Create Start instance and return working bot
    _final = CharmCord(
        prefix,
        case_insensitive,
        intents,
        activity,
        load_command_dir
    )
    if activity is not None:
        print("[CHARMCORD LOGS] Statuses successfully loaded")
    return _final
