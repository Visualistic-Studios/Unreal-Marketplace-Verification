#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   


########## BUILT-IN
#####
import os
from dotenv import load_dotenv
load_dotenv()
import random
import datetime

########## PIP
#####
from pysqlcipher3 import dbapi2 as sqlite3


########## CUSTOM
#####
from resources.config import app_config

# __     __              _         _      _            
# \ \   / /  __ _  _ __ (_)  __ _ | |__  | |  ___  ___ 
#  \ \ / /  / _` || '__|| | / _` || '_ \ | | / _ \/ __|
#   \ V /  | (_| || |   | || (_| || |_) || ||  __/\__ \
#    \_/    \__,_||_|   |_| \__,_||_.__/ |_| \___||___/
# ----------------------------------------------------------------------- 



##### SETTINGS
settings = app_config()



#  _____                      _    _                    
# |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
# ----------------------------------------------------------------------- 


###############
#####
##### DB
#####
###############


########## INITIATE 
#####
def initiate_database():

    """
    Initiates the connection. 
    """

    ##### CONNECT
    conn = sqlite3.connect(settings.full_database_file)

    ##### OPEN 
    c = conn.cursor()
    c.execute(f"PRAGMA key='{settings.db}'")

    if conn:
        return conn
    else:
        return None, None

    

########## CLOSE 
#####
def close_database(db_conn, should_save=False):

    ## SAVE
    if should_save:
        db_conn.commit()

    ## CLOSE
    if db_conn:
        db_conn.close()
        


###############
#####
##### INTERACTABLES
#####
###############



########## GET ALL INTERACTABLES
#####
def get_all_interactables():

    db_conn = initiate_database() 

    interactables_list = []

    for row in db_conn.execute("SELECT * FROM interactables"):
        interactables_list.append(row)

    close_database(db_conn)
    
    return interactables_list



########## GET INTERACTABLE IDS
#####  
def get_all_interactable_ids():
    
    interactable_ids_list = []

    for interactable in get_all_interactables():
        interactable_ids_list.append(interactable[1])

    return interactable_ids_list
    


########## IS INTERACTABLE
#####  
def is_interactable(int_id):
    return int(int_id) in get_all_interactable_ids() 
    

########## ADD INTERACTABLE
#####  
def add_interactable(uid):
    """
    Adds a user to the interactables list by Discord ID
    """
    ## Create connection
    db_conn = initiate_database()

    if not is_interactable(uid):

        ## Calc index
        new_index = len(get_all_interactable_ids()) + 1

        ## Execute Insert
        db_conn.execute("INSERT INTO interactables values(:new_index, :uid, 0)", {'new_index':new_index, 'uid':uid})
        ## Cleanup & Save
        close_database(db_conn, True)
    else:
        close_database(db_conn, True)


########## REMOVE INTERACTABLE BY INDEX
#####  
def remove_interactable_by_index(index):

    db_conn = initiate_database()

    db_conn.execute("DELETE FROM interactables WHERE index=':index'", {'index' : index})

    close_database(db_conn, True)


########## REMOVE INTERACTABLE BY UID
#####  
def remove_interactable_by_uid(uid):
    
    db_conn = initiate_database()

    db_conn.execute("DELETE FROM interactables WHERE user_id=:uid", {'uid' : int(uid)})

    close_database(db_conn, True)


def get_interactable_state(uid):

    db_conn = initiate_database()

    reward_state = None

    for row in db_conn.execute("SELECT * FROM interactables WHERE user_id=:uid", {'uid' : int(uid)}):
        reward_state = row[2]

    close_database(db_conn, False)

    return reward_state


def set_interactable_state(uid, new_state):

    db_conn = initiate_database()

    reward_state = None

    for row in db_conn.execute("UPDATE interactables SET current_reward_state=:new_state WHERE user_id=:uid", {'new_state':int(new_state), 'uid' : int(uid)}):
        reward_state = row[2]

    close_database(db_conn, True)

    return reward_state


###############
#####
##### BLOCKLIST
#####
###############

def get_all_blocklist_ids():

    db_conn = initiate_database()

    blocklist_list = []

    for row in db_conn.execute("SELECT user_id FROM bot_blocklist"):
        blocklist_list.append(row[0])

    close_database(db_conn, True)

    return blocklist_list


def is_blocklisted(uid):

    """
    Checks to see if a UID is blocklisted. Returns True/False
    """

    return uid in get_all_blocklist_ids()


def add_user_to_blocklist(uid):

    db_conn = initiate_database()

    new_index = len(get_all_blocklist_ids()) + 1

    db_conn.execute("INSERT INTO bot_blocklist values(:new_index, :uid)", {'new_index':new_index, 'uid':uid})

    close_database(db_conn, True)



def remove_user_from_blocklist(uid):

    db_conn = initiate_database()
    
    db_conn.execute("DELETE FROM bot_blocklist where user_id=:uid", {'uid':uid})

    close_database(db_conn, True)


###############
#####
##### CUSTOMER VERIFICATION
#####
###############

########## ADD UNVERIFIED CUSTOMER
#####
def add_unverified_customer(invoice="0000000", order_number="0000000", products=["DEFAULT VALUE"], discord_id="0000000000000000000", email="no@email.com"):

    db_conn = initiate_database()

    products = str(products)

    db_conn.execute("INSERT INTO customer_product_verification values(:invoice, :order_number, :products, :discord_id, :email, 'n/a')", {'invoice':invoice, 'order_number':order_number, 'products':products, 'discord_id':discord_id, 'email':email})

    close_database(db_conn, True)


########## GET ALL CUSTOMERS
#####
def get_all_customers():

    db_conn = initiate_database()
    post_list = []

    for row in db_conn.execute("SELECT * FROM customer_product_verification"):
        post_list.append(row)

    close_database(db_conn)

    return post_list



########## GET ALL UNVERIFIED CUSTOMERS
#####
def get_all_unverified_customers():

    db_conn = initiate_database()
    post_list = []

    for row in db_conn.execute("SELECT * FROM customer_product_verification WHERE is_verified='n/a'"):
        post_list.append(row)

    close_database(db_conn)

    return post_list


########## GET ALL VERIFIED CUSTOMERS
#####
def get_all_verified_customers():

    db_conn = initiate_database()
    post_list = []

    for row in db_conn.execute("SELECT * FROM customer_product_verification WHERE is_verified='yes'"):
        post_list.append(row)

    close_database(db_conn)

    return post_list

########## GET ALL UNVERIFIED CUSTOMERS
#####
def get_all_unverified_invoices():

    db_conn = initiate_database()
    post_list = []

    for row in db_conn.execute("SELECT invoice FROM customer_product_verification WHERE is_verified='n/a'"):
        post_list.append(str(row[0]))
        print(str(row[0]))

    close_database(db_conn)

    return post_list



########## GET ALL VERIFIED CUSTOMERS
#####
def get_all_verified_invoices():

    db_conn = initiate_database()
    post_list = []

    for row in db_conn.execute("SELECT invoice FROM customer_product_verification WHERE is_verified='yes'"):
        post_list.append(row[0])

    close_database(db_conn)

    return post_list


########## GET INVOICE DISCORD ID
#####
def get_invoice_discord_id(invoice_id):

    db_conn = initiate_database()
    discord_id = ""

    for row in db_conn.execute("SELECT discord_id FROM customer_product_verification WHERE invoice=:invoice", {'invoice':invoice_id}):
        discord_id = str(row[0])

    close_database(db_conn)

    return discord_id



########## GET INVOICE PRODUCTS
#####
def get_invoice_products(invoice_id):

    db_conn = initiate_database()
    products = None

    for row in db_conn.execute("SELECT product FROM customer_product_verification WHERE invoice=:invoice", {'invoice':invoice_id}):
        products = row[0]
        
    close_database(db_conn)

    print(f"products: {products}")
    products = products.strip("'")
    products = products.strip("]")
    products = products.strip("[")
    products = products.split(",")

    return products



########## MARK CUSTOMER VERIFIED
#####
def mark_customer_verified(invoice_id):

    db_conn = initiate_database()

    db_conn.execute("UPDATE customer_product_verification SET is_verified='yes' WHERE invoice=:invoice", {'invoice':invoice_id})

    close_database(db_conn, True)


########## MARK CUSTOMER NON VERIFIED
#####
def mark_customer_nonverified(invoice_id):

    db_conn = initiate_database()

    print('mark non verified')

    db_conn.execute("UPDATE customer_product_verification SET is_verified='no' WHERE invoice=:invoice", {'invoice':invoice_id})

    close_database(db_conn, True)

