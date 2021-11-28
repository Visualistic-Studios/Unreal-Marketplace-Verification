
#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------  


from resources.database import is_blocklisted
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



######## GET MEMBER AUTHORITY
#####
def get_member_authority(member):
    """
    Gets the authority of a member.

    Returns a string of "admin", "mod", or "default" depending on user's role.
    """
    
    object_is_member = None

    try:
        user_roles = member.roles
        if user_roles:
            object_is_member = True
    except Exception as e:
        object_is_member = False


    ##### MEMBER
    if object_is_member:
    
        ##### GET MEMBER ROLES
        user_roles = member.roles
        role_ids = []

        ##### CONVERT ROLES TO NAME LIST
        for role in user_roles:
            role_ids.append(role.id)


        ##### FIND CORRECT RETURN
        if role_ids.__contains__(settings.admin_role_id):
            authority_return = "admin"
            return authority_return
        elif role_ids.__contains__(settings.mod_role_id):
            authority_return = "mod"
            return authority_return
        else:
            authority_return = "default"
            return authority_return
    else:
        return "invalid"



######## IS MEMBER AUTHORITY
#####
def is_member_authority(member, authority_level="default"):
    if get_member_authority(member)==authority_level:
        return True
    else:
        return False


def is_user_blocklisted(user_id):
    return is_blocklisted(user_id)


