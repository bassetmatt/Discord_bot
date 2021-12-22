#Libraries to load the .env file
import os
from dotenv import load_dotenv
#Discord library
from discord.ext import commands

#Imports from other files
from src.youtube import *
from src.bot_commands import *

def main() :
    #Loads the environment variables
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
    #Bot setup
    bot = commands.Bot(COMMAND_SYMBOL, description='Yet another music bot.')
    bot.add_cog(Music(bot))

    #Confirms the login of the bot
    @bot.event
    async def on_ready():
        print(f'Logged in as:\n Username : {bot.user.name} \n Id : {bot.user.id}')

    bot.run(DISCORD_TOKEN)


# URL : https://discord.com/api/oauth2/authorize?client_id=921826543146254376&permissions=277028657216&scope=bot