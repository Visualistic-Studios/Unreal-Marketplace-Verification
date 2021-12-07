



#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------  

########## BUILT-IN
#####
import datetime


########## DISCORD
#####
import discord

########## SETTINGS
#####

from resources.config import app_config
import resources.verification as app_verify
import resources.database as app_database

# __     __              _         _      _            
# \ \   / /  __ _  _ __ (_)  __ _ | |__  | |  ___  ___ 
#  \ \ / /  / _` || '__|| | / _` || '_ \ | | / _ \/ __|
#   \ V /  | (_| || |   | || (_| || |_) || ||  __/\__ \
#    \_/    \__,_||_|   |_| \__,_||_.__/ |_| \___||___/
# ----------------------------------------------------------------------- 

########## SETTINGS
#####
settings = app_config()


#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# ----------------------------------------------------------------------- 



######## INITIATE REWARDSS
#####
async def command_request_verification(client,message):

    ## PARSE COMMAND
    local_split_message = str(message.content).strip(settings.command_prefix).split(" ")
    author = message.author
    print(f'initiating step one of verification for user {author.display_name}')
    try:
        await app_verify.initiate_discord_verification(client,author)
    except Exception as e:
        if '50007' in str(e):
            print("User doesn't allow messages")
            await message.channel.send(f"{author.mention}{settings.bot_message_user_direct_message_not_allowed}")

    
    print(f'step one of verification for user {author.display_name} is now complete')


######## SEND HELP COMMAND
#####
async def command_add_user_to_blocklist(message):

    ## FORMAT MESSAGE & EXTRACT CONTENTS
    local_split_message = str(message.content).strip(settings.command_prefix).split(" ")
    local_user_id = int(local_split_message[1])
    app_database.add_user_to_blocklist(local_user_id) ## takes a discord id 

    await message.channel.send(f"User `{local_user_id}` added to blocklist")



