import discord
from discord.ext import commands
from core.bot import Bot  # Assuming you have a custom Bot class in core.bot

if __name__ == '__main__':
    bot = Bot()  # Create an instance of your Bot class
    bot.run('Your Token')  # Replace 'Your Token' with your actual bot token
