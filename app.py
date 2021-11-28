
#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------  


######## BUILT-IN
#####
import os
import re 
from dotenv import load_dotenv
load_dotenv()


######## 3RD PARTY
#####
import discord
from discord.ext import commands, tasks



######## CUSTOM
#####
from resources.verification import verification_loop
from resources.config import app_config
from resources.database import is_blocklisted, is_interactable, get_interactable_state
from resources.commands import *
from resources.auth import is_member_authority



# __     __              _         _      _            
# \ \   / /  __ _  _ __ (_)  __ _ | |__  | |  ___  ___ 
#  \ \ / /  / _` || '__|| | / _` || '_ \ | | / _ \/ __|
#   \ V /  | (_| || |   | || (_| || |_) || ||  __/\__ \
#    \_/    \__,_||_|   |_| \__,_||_.__/ |_| \___||___/
# ----------------------------------------------------------------------- 


######## SETTINGS
#####
settings = app_config()

######## DISCORD
#####
bot_is_connected = False

if settings.is_testing:
    client = discord.Client(description='Hi', status=discord.Status.offline)
else:
    client = discord.Client()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=settings.command_prefix, intents=intents)


#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# ----------------------------------------------------------------------- 



######## NOTIFY ADMINS
#####
async def notify_admins(messageContent):
    channel = client.get_channel(int(settings.bot_log))
    await channel.send(str(messageContent))



######## TRY DO COMMAND
#####
async def try_do_command(message):
    try:
        message_string = str(message.content).split(" ")
        local_command = message_string[0].strip(str(settings.command_prefix)).lower()
        message_author = message.author

        # IF MOD
        if len(message_string) > 0 and is_member_authority(message_author, "mod") or is_member_authority(message_author, "admin"):
            ##### INITIATE ADD TO BLOCKLIST
            if settings.aliases_add_to_blocklist.__contains__(local_command):
                await command_add_user_to_blocklist(message)
            
        # ELSE IF BOT INTERACTION CHANNEL
        if message.channel.id == settings.bot_interaction or message.channel.id == settings.bot_interaction_testing:

            ##### INITIATE REQUEST VERIFICATION
            if settings.aliases_request_verification.__contains__(local_command):
                await command_request_verification(client, message)

    except Exception as the_error:
        await notify_admins(f"**COMMANDS** | User `{message_author}` (`{message.author.id}`) used command `{message.content}` in `{message.channel}` (`{message.channel.id}`)\nThere was an Error:\n```{the_error}```")



######## ON MESSAGE
#####
@client.event
async def on_message(message):

    ##### ONLY ALLOW MESSAGES FROM VALID USERS
    if is_blocklisted(message.author.id):
        pass

    ##### IF IN GUILD
    elif message.guild:

        ##### LOG MESSAGE STRING
        message_string = str(message.content)

        ##### COMMANDS
        if message_string.startswith(settings.command_prefix):
            await try_do_command(message)

    ##### IF A DM FROM AN AUTHORIZED USER
    elif is_interactable(message.author.id):
        await notify_admins(f"**INTERACTION REPLY** | User `{message.author}` (`{message.author.id}`) messaged the bot with the content: `{message.content}`")

    else:
        await notify_admins(f"**RANDOM MESSAGE** | User `{message.author}` (`{message.author.id}`) messaged the bot with the content: `{message.content}`")



########## COG LOOP
#####
class TimeLoopCog(commands.Cog):
    def __init__(self, something):
        while True:
            if client:
                self.product_verification_loop.start()
                break

    def cog_unload(self):
        self.product_verification_loop.cancel()


    @tasks.loop(seconds=settings.product_verification_loop_seconds)
    async def product_verification_loop(self):
        if len(client.guilds) > 0:
            await verification_loop(client.guilds[0])





#     _                   _  _               _    _               
#    / \    _ __   _ __  | |(_)  ___   __ _ | |_ (_)  ___   _ __  
#   / _ \  | '_ \ | '_ \ | || | / __| / _` || __|| | / _ \ | '_ \ 
#  / ___ \ | |_) || |_) || || || (__ | (_| || |_ | || (_) || | | |
# /_/   \_\| .__/ | .__/ |_||_| \___| \__,_| \__||_| \___/ |_| |_|
#          |_|    |_|                                             
# -----------------------------------------------------------------------


##### START APPLICATION
TimeLoopCog = TimeLoopCog(commands.Cog)
client.run(settings.discord_key)

