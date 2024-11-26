from discord.ext import commands
from utils.config import DEFAULT_PREFIX


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Replies with Pong!"""
        await ctx.send("Pong!")


async def setup(bot):
    await bot.add_cog(Test(bot))
