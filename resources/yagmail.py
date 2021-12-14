#  ___                                 _        
# |_ _| _ __ ___   _ __    ___   _ __ | |_  ___ 
#  | | | '_ ` _ \ | '_ \  / _ \ | '__|| __|/ __|
#  | | | | | | | || |_) || (_) || |   | |_ \__ \
# |___||_| |_| |_|| .__/  \___/ |_|    \__||___/
#                 |_|                           
# -----------------------------------------------------------------------   


from imap_tools import MailBox, AND, MailMessageFlags
import yagmail
import os
from dotenv import load_dotenv
load_dotenv()


from resources.config import app_config
from resources.crypt import hash_string



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

########## INITIATE MAILBOX
#####
def initiate_mailbox(read_only=True):
    if read_only:
        return MailBox(settings.email_server).login(settings.verification_email, settings.k_g_p)
    else:
        return yagmail.SMTP(settings.verification_email, settings.k_g_p)



########## CLOSE MAILBOX
#####
def close_mailbox(mailbox):
    try:
        mailbox.logout()
    except:
        pass



########## GET ALL EMAILS
#####
def get_all_emails(mailbox):
    """
    Returns emails in a [Invoice, Content] format
    """
    emails = []

    for msg in mailbox.fetch(bulk = True):
        emails.append([msg.subject.strip("Invoice #").strip(" "), msg.html])

    return emails



########## GET UNSEEN EMAILS
#####
def get_unseen_emails(mailbox):
    emails = []

    
    for msg in mailbox.fetch(AND(seen=False),bulk = True):
        emails.append([msg.subject, msg.html])

    return emails
    

########## SEND NEW VERIFICATION EMAIL
#####
def send_new_verification_email(mailbox,invoice_id="0000000", order_number="0000000", products=["DEFAULT VALUE"], discord_id="0000000000000000000", email="no@email.com"):

    new_product_append_string = ""

    ## CREATE PRODUCT STRING
    for product in products:
        if product == products[0]:
            new_product_append_string = product + ", "
        elif product == products[-1]:
            new_product_append_string = new_product_append_string + product
        else:
            new_product_append_string = new_product_append_string + product + ", "

    ## CREATE MESSAGE
    verify_message = settings.verify_message + f"""\n\n<b>Order #{order_number}</b>\n<b>Invoice #{invoice_id}</b>\n<b>Email: {email}\n<b>Products Purchased: {new_product_append_string}</b>\n\n------------------------------------------------------------------"""

    ## ADD TO MESSAGE IF TESTING
    if settings.is_testing:
        verify_message += """\n\n <h2><b> You've probably noticed this is test data</b></h2>\nThat's because this is a test! Please, if you can, simply respond as you normally would: "NO"\n Thank you for helping us create a quicker process for validating users!"""


    ## SEND
    mailbox.send(settings.epic_email, contents=verify_message, subject=f"Invoice #{invoice_id}")



########## TRY FIND EMAIL REPLY
#####
def try_find_email_reply(mailbox,invoice_id="0000000"):
    email = None
    emails = get_all_emails(mailbox)

    for subject, content in emails:
        if f"Invoice #{invoice_id}" in subject:
            email = [subject,content]
            break
    
    return email


########## TRY FIND UNSEEN EMAIL REPLY
#####
def try_find_unseen_email_replies(mailbox,invoice_ids=["0000000"]):
    email = None
    emails = get_unseen_emails(mailbox)
    new_emails = []

    for subject, content in emails:
        for invoice_id in invoice_ids:

            ## Split at #
            subject_clean = str(subject.split("#")[1])
            

            # # Stips email subject content to reveal the invoice
            # for to_replace in settings.email_strings_to_strip:
            #     subject_clean = subject.strip(to_replace)
            # print(f"clean pre-hash: {subject_clean}")

            ## HASH INVOICE
            subject_hash = hash_string(subject_clean)
            if invoice_id in subject_hash:
                new_emails.append([subject,content])
                break
    
    return new_emails



########## END BOT MESSAGE
#####
def check_verification_status(mailbox,invoice_ids=["0000000"]):

    ## CHECK FOR EMAIL REPLY
    email_replies = try_find_unseen_email_replies(mailbox, invoice_ids)
    confirmations_found = []

    ## IF REPLY EXISTS
    
    if email_replies:
        for reply in email_replies:

            reply_confirmation = None
            
            ## LOOK FOR CONFIRMATION
            for confirmation in settings.epic_confirmation_responses:
                if confirmation in reply[1]:
                    ## RETURN INVOICE & VALIDATION BOOL

                    id_reply = reply[0].split('#')[1]

                    print(f"'Clean' id reply: {id_reply}")

                    confirmations_found.append([id_reply, True])
                    reply_confirmation = True
                    break
            
            ## LOOK FOR NON CONFIRMATION
            if reply_confirmation == None:
                for non_confirmation in settings.epic_non_confirmation_responses:
                    if non_confirmation in reply[1]:    
                        ## RETURN INVOICE & VALIDATION BOOL

                        id_reply = reply[0].split('#')[1]

                        print(f"'Clean' id reply: {id_reply}")

                        confirmations_found.append([id_reply, False])
                        reply_confirmation = False
                        break
            
            ## NO RESPONSE RECOGNIZED
            if reply_confirmation == None:
                confirmations_found.append([reply[0], None])
                break

            ## IF NEITHER WERE FOUND, RETURN NONE (MESSAGE ADMINS ON OTHER SIDE)
        return confirmations_found

