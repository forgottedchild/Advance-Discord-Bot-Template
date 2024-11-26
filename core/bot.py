import discord
from discord.ext import commands
import os
from utils.config import DEFAULT_PREFIX, BOT_STATUS, ACTIVITY_TYPE, STATUS_TEXT


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.all()
        activity = discord.Activity(
            name=STATUS_TEXT.format(prefix=DEFAULT_PREFIX),
            type=getattr(discord.ActivityType, ACTIVITY_TYPE.lower(), discord.ActivityType.playing),
        )
        super().__init__(
            command_prefix=DEFAULT_PREFIX,
            intents=intents,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
            status=getattr(discord.Status, BOT_STATUS.lower(), discord.Status.online),
            activity=activity,
            strip_after_prefix=True,
            shard_count=kwargs.get("shard_count", 1),
            help_command=None,
        )
        self.db = None

    async def setup_hook(self):
        """
        Handles bot setup tasks such as loading extensions and preparing the bot.
        """
        # Load database connection if needed
        # self.db = await aiosqlite.connect("path_to_db.db")

        # Load Jishaku (for debugging)
        try:
            await self.load_extension("jishaku")
            print(" ❯ Loaded Jishaku successfully.")
        except Exception as e:
            print(f"Failed to load Jishaku: {e}")

        # Load extensions from specified directories
        await self.load_cogs_from_directory("cogs/handlers", "cogs.handlers")
        await self.load_cogs_from_directory("cogs/commands/utility", "cogs.commands.utility")
        await self.load_cogs_from_directory("cogs/commands/moderation", "cogs.commands.moderation")
        await self.load_cogs_from_directory("cogs/commands/extras", "cogs.commands.extras")
        await self.load_cogs_from_directory("cogs/commands/owner", "cogs.commands.owner")

    async def load_cogs_from_directory(self, directory: str, package: str):
        """
        Loads all cog files from the specified directory.
        :param directory: Directory path to search for cog files.
        :param package: Package name to use for the extensions.
        """
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist. Skipping.")
            return

        for file in os.listdir(directory):
            if file.endswith(".py") and not file.startswith("__"):
                extension = f"{package}.{file[:-3]}"
                try:
                    await self.load_extension(extension)
                    print(f" ❯ Successfully loaded {extension}.")
                except Exception as e:
                    print(f"Failed to load extension {extension}: {e}")

    async def on_ready(self):
        """
        Fired when the bot is ready.
        """
        print(f"Successfully connected as {self.user}.")
        print(f"Bot is ready and running on {len(self.guilds)} guilds.")
