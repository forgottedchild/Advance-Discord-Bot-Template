import discord
from discord.ext import commands


class MentionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots, including the bot itself
        if message.author.bot:
            return

        # Check if the bot is directly mentioned in the message
        if message.content.strip() == f"<@{self.bot.user.id}>":
            await message.channel.send("Heyyy!")

        # Allow other commands to work (critical if on_message is used)
        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(MentionEvent(bot))
