#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   


# add resources to this when you do the bot
from resources.config import app_config
from resources.crypt import hash_string
import resources.database as app_database
import resources.yagmail as app_verify
import resources.products as app_products
import discord
import asyncio


from time import sleep


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


########## CHECK FOR CANCELATION
#####
def check_for_cancelation(message_contents):
    if str(message_contents) in settings.allowed_cancelations:
        return True
    else:
        return False
        


########## SEND DISCORD CANCELATION NOTICE
#####
async def send_discord_cancelation_notice(discord_user):
    embed=discord.Embed()
    embed.add_field(name="Canceled", value="Verification Process Canceled. Please use the `!verify` command in the bot interaction channel in order to restart the process. Have a great day! :)", inline=False)
    return await discord_user.send(embed=embed)



########## SEND DISCORD INVALID INVOICE NOTICE
#####
async def send_invalid_discord_invoice_notice(discord_user):
    embed=discord.Embed()
    embed.add_field(name="Invalid Invoice", value="An invalid invoice was detected; invoices should be 11 characters long. Please check to make sure your ID is correct. If you believe this is a mistake, reach out to an admin in the server. Thank you!", inline=False)
    return await discord_user.send(embed=embed)



########## SEND INVALID ORDER NOTICE
#####
async def send_invalid_discord_order_id_notice(discord_user):
    embed=discord.Embed()
    embed.add_field(name="Invalid Order", value="An invalid order was detected; orders should be 17 characters long. Please check to make sure your ID is correct. If you believe this is a mistake, reach out to an admin in the server. Thank you!", inline=False)
    return await discord_user.send(embed=embed)



########## SEND INVALID PRODUCTS
#####
async def send_invalid_discord_products_notice(discord_user):
    embed=discord.Embed()
    embed.add_field(name="Invalid Products", value="Please select one of the IDs mentioned above", inline=False)
    return await discord_user.send(embed=embed)



########## SEND DISCORD SUCCESSFUL INITIATION NOTICE
#####
async def send_discord_successful_initiation_notice(discord_user):
    embed=discord.Embed()
    embed.add_field(name="Success!", value="Thank you! You'll be notified when Epic has responded. (Hopefully, pretty soon!) Thanks for your purchase, and welcome to the community if you're new <3", inline=False)
    return await discord_user.send(embed=embed)






########## SEND DISCORD PRODUCT VERIFY INITIAL NOTICE
#####
async def send_discord_product_verify_initial_notice(discord_user):
    ## MESSAGE |  OVERVIEW
    embed = discord.Embed()
    embed.add_field(name="Product Verification", value="Hello there! We've created a tool that will automatically reach out to Epic with your details to save you time getting support with your products. Please, enter accurate information and read carefully. Process is canceled after 90 second idle.", inline=False)
    embed.add_field(name="Step 1 | Receiving your Information", value="First things first, we need to get some information about your order. We'll use this to verify your order with Epic. You can find all of the necessary information in your order email, which you should probably have open!", inline=False)
    embed.add_field(name="Step 2 | Waiting for Verification", value="After we've sent your information to Epic, there will be a short wait (typically within 24h) while we wait for their response. ", inline=False)
    embed.add_field(name="Step 3 | Verification Complete", value="Once Epic has responded, I'll immediately assign you the proper roles & let you know with a message.", inline=False)
    embed.set_footer(text=settings.privacy_policy)
    await discord_user.send(embed=embed)

    ## MESSAGE | PREPERATION
    embed=discord.Embed()
    embed.add_field(name="For this next step", value="Please have the email from Epic open in the background. Reply with anything when you're ready to start the process. Reply with `cancel` at any time to cancel the process.", inline=False)
    await discord_user.send(embed=embed)



########## GET CUSTOMER INITIAL RESPONSE
#####
async def get_discord_customer_initial_response(bot_client, discord_user, bot_reset):

    ## NONE = NEED TO REPEAT
    ## FALSE = CANCELED
    ## TRUE = VALID INPUT

    ## MESSAGE | ASK FOR RESPONSE
    if not bot_reset:               ## Message may get reset, hence why it's on a loop. If reset is true, it will skip messaging the user
         await send_discord_product_verify_initial_notice(discord_user)

    response_msg = None

 ## WAIT FOR RESPONSE
    try:
        response_msg = await bot_client.wait_for('message', timeout=settings.product_verification_reply_timeout)
    except asyncio.TimeoutError:
        await send_discord_cancelation_notice(discord_user)
        return False
    else:
        ## CORRECT USER ID?
        if int(response_msg.author.id)==int(discord_user.id):
            ## CHECK FOR CANCELATION
            response_msg = response_msg.content
            if "'" in response_msg:
                response_msg = response_msg.strip("'")
            if '"' in response_msg:
                response_msg = response_msg.strip('"')

            if not check_for_cancelation(response_msg):
                return True
            ## CANCELED
            else:
                await send_discord_cancelation_notice(discord_user)
                return False
        else:
            print('Being messaged by an invalid user')
            ## INVALID RESPONSE (NOT FROM DESIRED USER)
            return None




########## GET DISCORD CUSTOMER INVOICE
#####
async def get_discord_customer_invoice(bot_client, discord_user, bot_reset):

    ##### RETURNS
    ## NONE = NEED TO REPEAT
    ## FALSE = CANCELED
    ## TRUE = VALID INPUT

    ## MESSAGE | ASK FOR INVOICE
    if not bot_reset:               ## Message may get reset, hence why it's on a loop. If reset is true, it will skip messaging the user
        embed=discord.Embed()
        embed.add_field(name="Invoice ID", value="""Please reply with the Invoice ID in your email. Looks like "F9999999999" without the quotes""", inline=False)
        await discord_user.send(embed=embed)


    try:
        response_msg = await bot_client.wait_for('message', timeout=settings.product_verification_reply_timeout)
    except asyncio.TimeoutError:
        await send_discord_cancelation_notice(discord_user)
        return False
    else:
        ## CORRECT USER ID?
        if int(response_msg.author.id)==int(discord_user.id):
            ## STRIP OF ANY QUOTES
            response_msg = response_msg.content
            if "'" in response_msg:
                response_msg = response_msg.strip("'")
            if '"' in response_msg:
                response_msg = response_msg.strip('"')

            ## CHECK FOR CANCELATION
            if not check_for_cancelation(response_msg):
                ## CHECK FOR PROPER LENGTH
                response_msg_list=list(response_msg)
                if len(response_msg_list)>=9:
                    return response_msg
                else:
                    ## INVALID RESPONSE
                    await send_invalid_discord_invoice_notice(discord_user)
                    return None
            ## CANCELED
            else:
                await send_discord_cancelation_notice(discord_user)
                return False
        else:
            ## INVALID RESPONSE (NOT FROM DESIRED USER)
            return None






########## GET DISCORD CUSTOMER ORDER ID
#####
async def get_discord_customer_order_id(bot_client, discord_user, bot_reset):

    ##### RETURNS
    ## NONE = NEED TO REPEAT
    ## FALSE = CANCELED
    ## TRUE = VALID INPUT

    ## ## MESSAGE | ASK FOR ORDER ID
    if not bot_reset:
        embed=discord.Embed()
        embed.add_field(name="Order ID", value="""Please reply with the Order ID in your email. Looks like "F9999999999999999" without the quotes""", inline=False)
        await discord_user.send(embed=embed)

    try:
        response_msg = await bot_client.wait_for('message', timeout=settings.product_verification_reply_timeout)
    except asyncio.TimeoutError:
        await send_discord_cancelation_notice(discord_user)
        return False
    else:
        ## CORRECT USER ID?
        if int(response_msg.author.id)==int(discord_user.id):
            ## STRIP OF ANY QUOTES
            response_msg = response_msg.content
            if "'" in response_msg:
                response_msg = response_msg.strip("'")
            if '"' in response_msg:
                response_msg = response_msg.strip('"')

            ## CHECK FOR CANCELATION
            if not check_for_cancelation(response_msg):
                ## CHECK FOR PROPER LENGTH
                response_msg_list=list(response_msg)
                if len(response_msg_list)>=13:
                    return response_msg
                else:
                    ## INVALID RESPONSE
                    await send_invalid_discord_order_id_notice(discord_user)
                    return None
            ## CANCELED
            else:
                await send_discord_cancelation_notice(discord_user)
                return False
        else:
            ## INVALID RESPONSE (NOT FROM DESIRED USER)
            return None



########## GET DISCORD CUSTOMER PRODUCTS
#####
async def get_discord_customer_products(bot_client, discord_user, bot_reset):

    ##### RETURNS
    ## NONE = NEED TO REPEAT
    ## FALSE = CANCELED
    ## TRUE = VALID INPUT

    ## ## MESSAGE | ASK FOR PRODUCTS
    if not bot_reset:
        embed=discord.Embed()
        embed.add_field(name="Products", value="""Here are a list of our products. Please reply with the ID next to the ones listed in the order. If you have multiple products, seperate them by commas. If you purchased products in seperate orders, make sure to verify them seperately. | Response will look like "1,3" without the quotes""", inline=False)
        await discord_user.send(embed=embed)
        available_products_msg = app_products.build_available_products_string(True, True, False, True)               # Inputs: Print with IDs, Print with Newlines, Print with Commas, Discord Format (Adds ` before and after ID to highlight it)
        await discord_user.send(available_products_msg)


    try:
        response_msg = await bot_client.wait_for('message', timeout=settings.product_verification_reply_timeout)
    except asyncio.TimeoutError:
        await send_discord_cancelation_notice(discord_user)
        return False
    else:
        try:
        ## CORRECT USER ID?
            if int(response_msg.author.id)==int(discord_user.id):
                ## CHECK FOR CANCELATION
                if not check_for_cancelation(response_msg):
                    ## CHECK FOR PROPER LENGTH
                    response_msg = response_msg.content
                    if " " in response_msg:
                        response_msg = response_msg.strip(" ")
                    if "," in response_msg:
                        response_msg = response_msg.split(',')
                    else:
                        response_msg = [response_msg]
                    ## IF VALID RESPONSE FOUND
                    if response_msg:    
                        ## VALID RESPONSE
                        if response_msg[-1]==",":
                            del response_msg[-1]
                        ## CREATE LIST OF PRODUCT NAMES
                        product_name_list = []
                        last_product_index = len(settings.released_product_list)-1
                        for product in response_msg:    
                            ## CHECK IF IN RANGE
                            if int(product)>last_product_index:
                                return None
                            else:
                                ## GET NAME FROM ID
                                product_name = app_products.get_product_by_id(int(product))
                                product_name_list.append(product_name)
                                pass 
                        ## RETURN IT
                        return product_name_list
                    ## INVALID RESPONSE FOUND
                    else:
                        await send_invalid_discord_products_notice(discord_user)
                        return None
                ## CANCELED
                else:
                    await send_discord_cancelation_notice(discord_user)
                    return False
            else:
                ## INVALID RESPONSE (NOT FROM DESIRED USER)
                return None
        except:
            await send_invalid_discord_products_notice(discord_user)
            return None


########## GET DISCORD CUSTOMER EMAIL
#####
async def get_discord_customer_email(bot_client, discord_user, bot_reset):

    ##### RETURNS
    ## NONE = NEED TO REPEAT
    ## FALSE = CANCELED
    ## TRUE = VALID INPUT

    ## ## MESSAGE | ASK FOR EMAIL
    if not bot_reset:
        embed=discord.Embed()
        embed.add_field(name="Email", value="""Please reply with the email associated with the order. This will be shown in the invoice next to "Bill To:" """, inline=False)
        await discord_user.send(embed=embed)


    try:
        response_msg = await bot_client.wait_for('message', timeout=settings.product_verification_reply_timeout)
    except asyncio.TimeoutError:
        await send_discord_cancelation_notice(discord_user)
        return False
    else:
        ## CORRECT USER ID?
        if int(response_msg.author.id)==int(discord_user.id):
            ## STRIP OF ANY QUOTES
            response_msg = response_msg.content
            if "'" in response_msg:
                response_msg = response_msg.strip("'")
            if '"' in response_msg:
                response_msg = response_msg.strip('"')

            ## CHECK FOR CANCELATION
            if not check_for_cancelation(response_msg):
                ## CHECK FOR PROPER LENGTH
                return response_msg
            ## CANCELED
            else:
                await send_discord_cancelation_notice(discord_user)
                return False
        else:
            ## INVALID RESPONSE (NOT FROM DESIRED USER)
            return None



########## GET DISCORD CUSTOMER FINAL AUTH
#####
async def get_discord_customer_final_auth(bot_client, discord_user, bot_reset, order_info):

    ##### RETURNS
    ## NONE = NEED TO REPEAT
    ## FALSE = CANCELED
    ## TRUE = VALID INPUT

    ## ## MESSAGE | ASK FOR FINAL AUTH
    if not bot_reset:
        invoice = order_info[0]
        order_id = order_info[1]
        products = str(order_info[2])
        products = products.replace("','", " ")
        products = products.replace("[", "")
        products = products.replace("]", "")
        products = products.replace("'", "")
        email = order_info[3]

        await discord_user.send(f"`EMAIL` | **{email}**\n`ORDER ID` | **{order_id}**\n`INVOICE ID` | **{invoice}**\n`PRODUCTS` | **{products}**\n\n`?`")

        embed=discord.Embed()
        embed.add_field(name="Final Authorization", value="""Please review all the information above. If it's correct, answer with "yes". If not, say "no".""", inline=False)
        await discord_user.send(embed=embed)


    try:
        response_msg = await bot_client.wait_for('message', timeout=settings.product_verification_reply_timeout)
    except asyncio.TimeoutError:
        await send_discord_cancelation_notice(discord_user)
        return False
    else:
        ## CORRECT USER ID?
        if int(response_msg.author.id)==int(discord_user.id):
            ## STRIP OF ANY QUOTES
            response_msg = response_msg.content
            if "'" in response_msg:
                response_msg = response_msg.strip("'")
            if '"' in response_msg:
                response_msg = response_msg.strip('"')

            ## CHECK FOR CANCELATION
            if not check_for_cancelation(response_msg):
                ## CHECK FOR VALID RESPONSE    
                if response_msg:
                    if response_msg in settings.allowed_confirmations:
                        return True
                    elif response_msg in settings.allowed_non_confirmations:
                        return False
                else:
                    ## INVALID RESPONSE
                    return None
            ## CANCELED
            else:
                await send_discord_cancelation_notice(discord_user)
                return False
        else:
            ## INVALID RESPONSE (NOT FROM DESIRED USER)
            return None

   

########## START DISCORD INFORMATION REQUEST
#####
async def start_discord_information_request(bot_client, discord_user):

    invoice = None
    valid_invoice = False
    order_id = None
    valid_order_id = False
    products = []
    valid_products = False
    email = None
    valid_email = False
    valid_response = False
    discord_id = discord_user.id
    customer_has_validated = False
  

    bot_reset = None
    ## ------- INVOICE ------- ##
    while not valid_response:

        ## GET RESPONSE
        response = await get_discord_customer_initial_response(bot_client, discord_user, bot_reset)
        ## IF VALID INVOICE
        if response:
            valid_response=True
            bot_reset = None
        ## IF CANCELED/TIMEOUT
        elif response==False:
            valid_response = False
            return None
        ## IF INVALID rRESPONSE
        elif response==None:
            bot_reset = True
            pass



    ## ------- INVOICE ------- ##
    while not valid_invoice and valid_response:

        ## GET INVOICE
        invoice = await get_discord_customer_invoice(bot_client, discord_user, bot_reset)
        ## IF VALID INVOICE
        if invoice:
            valid_invoice=True
            bot_reset = None
        ## IF CANCELED/TIMEOUT
        elif invoice==False:
            valid_invoice = False
            return None
        ## IF INVALID INVOICE ID
        elif invoice==None:
            bot_reset = True
            pass


    ## ------- ORDER ID ------- ##
    while not valid_order_id and valid_invoice:
        ## GET ORDER ID
        order_id = await get_discord_customer_order_id(bot_client, discord_user, bot_reset)
        ## IF VALID ORDER ID
        if order_id:
            valid_order_id=True
            bot_reset = None
        ## IF CANCELED
        elif order_id==False:
            valid_order_id=False
            return None
        ## IF INVALID ORDER ID
        elif order_id==None:
            bot_reset = True
            pass



    ## ------- PRODUCTS ------- ##
    while not valid_products and not valid_order_id==False:
        ## GET PRODUCTS
        products = await get_discord_customer_products(bot_client, discord_user, bot_reset)
        ## IF VALID PRODUCTS
        if products:
            valid_products=True
            bot_reset = None
        ## IF CANCELED
        elif products==False:
            await send_discord_cancelation_notice(discord_user)
            valid_products=False
            return None
        elif products==None:
            bot_reset = True
            pass

    ## ------- EMAIL ------- ##
    while not valid_email and not valid_products==False:
        ## GET EMAIL
        email = await get_discord_customer_email(bot_client, discord_user, bot_reset)
        ## IF VALID EMAIL
        if email:
            valid_email=True
            bot_reset = None
        ## IF CANCELED
        elif email==False:
            await send_discord_cancelation_notice(discord_user)
            valid_email=False
            return None
        elif email==None:
            bot_reset = True
            pass

    while not customer_has_validated:
        ## AT THE END, CHECK IF ALL DATA IS CORRECT & VALIDATED
        if invoice and valid_invoice and order_id and valid_order_id and products and valid_products and email and valid_email:
            final_auth = await get_discord_customer_final_auth(bot_client, discord_user, bot_reset, [invoice, order_id, products, email])
            if final_auth:
                customer_has_validated = True
            elif final_auth == False:
                ## CANCELED 
                await send_discord_cancelation_notice(discord_user)
                return None
            else:
                bot_reset = True
                pass
        else:
            ## CANCELED
            await send_discord_cancelation_notice(discord_user)
            return None
    
    if customer_has_validated:
        await send_discord_successful_initiation_notice(discord_user)
        return invoice, order_id, products, discord_id, email




########## INITIATE DISCORD VERIFICATION
#####
async def initiate_discord_verification(bot_client, discord_user):

    ## ADD USER TO INTERACTABLE LIST
    app_database.add_interactable(discord_user.id)

    ## INITIATE MAILBOX
    mailbox = app_verify.initiate_mailbox(False)

    ## GET ALL DATA
    order_info = await start_discord_information_request(bot_client, discord_user)
    if order_info == False:

        ## PRODUCT VERIFICATION CANCELED
        app_database.remove_interactable_by_uid(discord_user.id)
        return False

    ## INVALID ORDER DATA/ERROR
    elif order_info == None:
        app_database.remove_interactable_by_uid(discord_user.id)
        return None

    ## ELSE IF INFO CORRECT
    else:
        invoice_id = order_info[0]
        order_id = order_info[1]
        products = order_info[2]
        discord_id = order_info[3]
        email = order_info[4]

        ## SEND EMAIL TO EPIC 
        app_verify.send_new_verification_email(mailbox, invoice_id,order_id, products, discord_id, email)
        
        ## LOG CUSTOMER AS UNVERIFIED
        app_database.add_unverified_customer(hash_string(invoice_id), hash_string(order_id), products, discord_id, hash_string(email))
        user_guild = await bot_client.fetch_guild(settings.guild_id)
        unverified_role = user_guild.get_role(settings.unverified_role_id)
        await discord_user.add_roles(unverified_role)

        # REMOVE AS INTERACTABLE
        app_database.remove_interactable_by_uid(discord_user.id)

        ## RETURN
        return True



########## VERIFICATION LOOP
#####
async def verification_loop(client, guild):

    mailbox = app_verify.initiate_mailbox()
    invoice_responses = app_verify.check_verification_status(mailbox, app_database.get_all_unverified_invoices())


    ## IF ANY RESPONSES TO OUR PREVIOUS EMAILS
    if invoice_responses:
        for response in invoice_responses:


            ## GET THE INVOICE FROM THE EMAIL
            if "Unreal Engine Marketplace - Invoice #" in response[0]:
                invoice = response[0].strip("Unreal Engine Marketplace - Invoice #")
            else:
                invoice = response[0].strip("Invoice #")

            invoice_hash = hash_string(invoice)

            print(f"Invoice Hash: {invoice_hash}")
            

            products_string = ""

            roles_to_assign = []

            role_to_assign = None

            ## GIVE USER ROLES
            for index, product in enumerate(app_database.get_invoice_products(invoice_hash)):
                role_to_assign = await app_products.get_product_role_by_name(product, guild)
                roles_to_assign.append(role_to_assign)


                if len(settings.released_product_list)>1:
                    if index==0:
                        products_string += "s " + str(product)
                    elif index==len(settings.released_product_list)-1:
                        products_string = products_string + f" and {str(product)}"
                    else:
                        products_string += ", " + str(product)
                else:
                    products_string = " " + str(product)

            products_string = products_string.replace("'", "")

            ## IF VALID
            if response[1]:
                ## CUSTOMER HAS BEEN VERIFIED
                app_database.mark_customer_verified(invoice_hash)


      
                user_receiving_roles_id = app_database.get_invoice_discord_id(invoice_hash)
                user_receiving_roles = guild.get_member(int(user_receiving_roles_id))

                for role in roles_to_assign:
                    if role:
                        await user_receiving_roles.add_roles(role)
                
                ## REMOVE UNVERIFIED ROLE
                await user_receiving_roles.remove_roles(settings.get_unverified_owner_role(guild))

                ## SEND THEM A VERIFICATION
                embed=discord.Embed()
                embed.add_field(name="Products Validated", value=f"Your order with the product{products_string} was validated by Epic! Check the Discord Community, you've got new roles!", inline=False)
                await user_receiving_roles.send(embed=embed)

                ## NOTIFY ADMINS
                ######## NOTIFY ADMINS
                bot_log_channel = client.get_channel(int(settings.bot_log))
                await bot_log_channel.send(f"User {user_receiving_roles.mention} has been validated by Epic. \n\nInvoice Hash: `{invoice_hash}`")


            ## INVALID INVOICE. CUSTOMER ENTERED INCORRECT DATA. REACH OUT TO ADMINS & MARK UNVERIFIED.
            elif response[1]==False:
                app_database.mark_customer_nonverified(invoice_hash)
                
                ## SEND MESSAGE TO USER
                user_id = app_database.get_invoice_discord_id(invoice_hash)
                user_object = guild.get_member(int(user_id))
                
                embed=discord.Embed()
                embed.add_field(name="Products Not Valid", value=f"Your order with the product{products_string} unfortunately wasn't validated by Epic. Please reach out to admins if you believe this is an error. ", inline=False)
                await user_object.send(embed=embed)

                ## SEND MESSAGE TO ADMINS
                notify_channel = guild.get_channel(settings.bot_log)
                embed=discord.Embed()
                embed.add_field(name="Products Not Valid", value=f"The user {user_object.display_name} ({user_object.id}) tried to verify with the product{products_string}\nUnfortunately, Epic said they were invalid.", inline=False)
                await notify_channel.send(embed=embed)

            ## ELSE RESPONSE NOT RECOGNIZED. NEED TO REACH OUT TO ADMINS WITH THE DETAILS
            else:
                pass
                # need to notify admin 

    app_verify.close_mailbox(mailbox)


