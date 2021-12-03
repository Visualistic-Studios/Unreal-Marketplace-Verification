
#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   


import os
import json
from configparser import ConfigParser
from dotenv import load_dotenv

load_dotenv()



# __     __              _         _      _            
# \ \   / /  __ _  _ __ (_)  __ _ | |__  | |  ___  ___ 
#  \ \ / /  / _` || '__|| | / _` || '_ \ | | / _ \/ __|
#   \ V /  | (_| || |   | || (_| || |_) || ||  __/\__ \
#    \_/    \__,_||_|   |_| \__,_||_.__/ |_| \___||___/
# ----------------------------------------------------------------------- 

config = ConfigParser()
current_directory = os.path.dirname(os.path.abspath(__file__)).strip("resources/")
config_file_path = "/" + str(current_directory) + "/config/config_production.ini"


#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# ----------------------------------------------------------------------- 

def read_config(category, key, config_path = config_file_path):
    config.read(config_path)
    if config_path:
        value = str(config.get(category, key))
        if value: 
            return value
        else:
            return None
    else:
        return None
    

def str_to_bool(string):
    if string in ["True"]:
        the_return = True
    else:
        the_return = False
    return the_return


########## CONFIGURATION CLASS
#####
class app_config: 

    ########## INIT
    #####
    def __init__(self): 

        ## CORE

        temp_current_directory = os.path.dirname(os.path.abspath(__file__))
        temp_current_directory_l = temp_current_directory.split("/")
        del temp_current_directory_l[-1]

        temp_is_testing = read_config("core", "is_testing")
        self.is_testing = str_to_bool(temp_is_testing)
        self.core_directory = '/'.join(temp_current_directory_l) + "/"
        self.privacy_policy = read_config("core", "privacy_policy")

        self.k_path = read_config('core_paths', 'sec_path') + "k.ini"


        ##### API KEY SWITCHING
        if self.is_testing:
            self.discord_key = str(read_config("pass", "k_t", self.k_path))
        else:
            self.discord_key = str(read_config("pass", "k_d", self.k_path))


        self.db = str(read_config("pass", "db", self.k_path))
        self.k_g_p = str(read_config("pass", "k_g_p", self.k_path))


        ## PATHS
        self.local_config_path = read_config("core_paths", "config_path")
        self.local_saved_path = read_config("core_paths", "saved_path")
        self.local_resources_path = read_config("core_paths", "resources_path")
        self.local_database_path = read_config("core_paths", "database_path")
        self.full_config_path = self.core_directory + self.local_config_path
        self.full_saved_path = self.core_directory + self.local_saved_path
        self.full_resources_path = self.core_directory + self.local_resources_path
        self.full_database_path = self.core_directory + self.local_database_path


        ## FILES
        self.local_database_file = read_config("core_paths", "database_file")
        self.local_config_file = read_config("core_paths", "config_file")
        self.local_yag_file = read_config("core_paths", "yag_file")
        self.full_database_file = self.core_directory + self.local_database_file
        self.full_config_file = self.core_directory + self.local_config_file
        self.full_yag_file = self.core_directory + self.local_yag_file


        ##### DISCORD SETTINGS
        self.command_prefix = read_config("discord_settings", "command_prefix")
        self.guild_id = read_config("discord_settings", "bot_guild_id")


        ##### DISCORD ROLES
        self.unverified_role_id = int(read_config("discord_roles", "unverified_role_id"))
        self.admin_role_id = int(read_config('discord_roles', 'admin_role_id'))
        self.mod_role_id = int(read_config('discord_roles', 'mod_role_id'))
        

        ##### DISCORD COMMANDS
        self.allowed_confirmations = read_config("discord_commands", "allowed_confirmations").split(",")
        self.allowed_non_confirmations = read_config("discord_commands", "allowed_non_confirmations").split(",")
        self.aliases_request_verification = read_config("discord_commands", "aliases_request_verification").split(",")
        self.allowed_cancelations = read_config("discord_commands", "allowed_cancelations").split(",")
        self.aliases_add_to_blocklist = read_config("discord_commands", "aliases_add_to_blocklist").split(",")
        

        ##### DISCORD CHANNELS
        self.bot_log = int(read_config("discord_channels", "bot_log"))
        self.bot_interaction = int(read_config("discord_channels", "bot_interaction"))
        self.bot_interaction_testing = int(read_config("discord_channels", "bot_interaction_testing"))


        ##### PRODUCT VERIFICATION
        self.epic_confirmation_responses = read_config("product_verification", "epic_confirmation_responses").split(",")
        self.epic_non_confirmation_responses = read_config("product_verification", "epic_non_confirmation_responses").split(",")
        self.product_verification_loop_seconds = int(read_config("product_verification", "product_verification_loop_seconds"))
        self.product_verification_reply_timeout = int(read_config("product_verification", "product_verification_reply_timeout"))
        self.verification_email = read_config("product_verification", "verification_email")
        self.email_server = read_config("product_verification", "email_server")
        self.released_product_list = read_config("core", "released_product_list").split(",")
        
        if self.is_testing:
            self.epic_email = self.verification_email
        else:
            self.epic_email = read_config("product_verification", "epic_email")

        self.verify_message = read_config('product_verification', 'email_verify_message').replace('\\n', '\n')

        self.email_strings_to_strip = read_config("product_verification", "email_strings_to_strip").split(",")


    ########## GET CHANNEL IDS
    #####

    ##### INTERACTION
    def get_bot_interaction_id(self):

        if self.is_testing:
                channel = self.bot_interaction_testing
        else:
                channel = self.bot_interaction
    
        return channel


    
    ########## GET CHANNEL OBJECTS
    #####

    ##### INTERACTION
    def get_bot_interaction_channel(self, client_or_guild):
        return client_or_guild.get_channel(self.get_bot_interaction_id())


    ##### UNVERIFIED OWNER 
    def get_unverified_owner_role(self, guild):
        return guild.get_role(self.unverified_role_id)

