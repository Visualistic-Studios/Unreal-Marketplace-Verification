#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   


from resources.config import app_config

# __     __              _         _      _            
# \ \   / /  __ _  _ __ (_)  __ _ | |__  | |  ___  ___ 
#  \ \ / /  / _` || '__|| | / _` || '_ \ | | / _ \/ __|
#   \ V /  | (_| || |   | || (_| || |_) || ||  __/\__ \
#    \_/    \__,_||_|   |_| \__,_||_.__/ |_| \___||___/
# ----------------------------------------------------------------------- 

settings = app_config()

#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# ----------------------------------------------------------------------- 



########## GET PRODUCT BY ID
def get_product_by_id(product_id):
    return settings.released_product_list[product_id]



########## GET PRODUCT ROLE BY NAME
#####
async def get_product_role_by_name(product_name, guild):
    local_role = None
    guild_roles = await guild.fetch_roles()
    clean_product_name = product_name.replace("'", "")
    
    for role in guild_roles:
        role_name = role.name
        #print(f"product name: {clean_product_name}\n\nrole name: {role_name}")
        if clean_product_name in role_name:
            local_role = role
            break
    return local_role
            
        

########## BUILD AVAILABLE PRODUCTS STRING
#####
def build_available_products_string(IDs=True,newlines=True,commas=False,discord_format=False):
    """
    Inputs: Print with IDs, Print with Newlines, Print with Commas, Discord Format (Adds ` before and after ID to highlight it)
    """
    
    products_string = ""

    if commas:
        comma_string = ", "
    else:
        comma_string = ""


    if newlines:
        newline_string = "\n"
    else:
        newline_string = ""

    if discord_format:
        discord_format_string = "`"
    else:
        discord_format_string = ""

    for index,product in enumerate(settings.released_product_list):

        if IDs:
            ID_string = f"{discord_format_string}{index}{discord_format_string} | "
        else:
            ID_string = f""

        ## IF FIRST INDEX
        if index==0:
            products_string = f"{ID_string}" + str(product) + comma_string + newline_string
        ## IF LAST INDEX
        elif index == len(settings.released_product_list)-1:
            products_string = products_string + f"{ID_string}" + str(product)
        ## IF OTHER INDEX
        else:
            products_string = products_string + f"{ID_string}" + str(product) + comma_string + newline_string

    return products_string


