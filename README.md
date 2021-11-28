# Unreal Engine Marketplace Verification
## Introduction
Most Unreal Engine Marketplace developers have a Discord community to provide support to their customers. In order to validate real customers, some turn to taking order information from customers and manually sending it to Marketplace Support for validation from Epic. They then assign the user a role which allows them to access support channels and be known as an officially verified owner. This is a tool for those developers to validate their customers automatically using a Discord bot & dedicated email account. 

## Functionality
The bot will request customer information on command though a direct message, sending a friend request first if they do not allow messages from server. It then forwards the information to Epic Marketplace Support, asks for validity, & waits for a response. 

`Valid Response`
- Let the user know through a direct message
- Assign user roles in the discord
- Mark user as verified in database & increment validation count. 

`Invalid Response` 
- Tell user in a direct message to reach out to an admin if they believe it's an error. 

Order information is stored as a hash for privacy. With the hashed data you can still monitor requests & enable instant future verification. `Discord ID` & `products owned` remain unhashed due to the bot need to know the users' ID & products owned to give the user the roles & interact with them after it's received a reply. 

Bot relays information provided to it in a `bot-log`, which can be monitored by a select group of admins / mods for support & security reasons. Messages are purged after (x) hours (72 by default) on a timer (every 15 minutes by default)


# TEMPORARY NOTES:

- Currently the project works, but isn't updated with a complete guide just yet. It also needs some work. I would love to make this a more reliable, secure, and complete solution. If you find yourself wanting to help, [join the Discord](https://discord.gg/FEnDUZ7rNK) & send me a message!

- Some of the features stated above are not implemented yet. Generally it's safe to assume if it's not on the issues list & it's mentioned here, it's implemented.

# Requirements
- Python 3
- PySQLCipher
- Email (Gmail out of the box)

# Setup

## 1. Install Python 3
- [Link to their website](https://www.python.org/download/releases/3.0/)

## 2. Install SQLite & PySQLCipher

**Linux**
```
## SQLCipher & dependencies
`sudo apt install sqlcipher libsqlcipher0 libsqlcipher-dev`

## Optional virtual environment
`python3 -m venv venv`

## Install the python wrapper
`pip3 install pysqlcipher3`
```

**Mac**
```py
brew install sqlite3

## Optional virtual environment
python3 -m venv venv

## Install the python wrapper
pip3 install pysqlcipher3
```

## 3. Create the Database

## 4. Gmail
It is recommended to create a new Gmail account specifically for the purpose of verifying your users. Don't sign up for anything using this account; keep it specific for this purpose. Give it a random, high entropy password.

- Go to your account settings. Navigate to the `Security` tab. 
- Scroll down until you find `Less secure app access`, turn it `ON`

## 5. Discord
**Create the Bot**
- Create the bot on [Discord's Developer Panel](https://discord.com/developers/applications). Give it a name & an icon. 

- Under the `Bot` tab, create the bot & give it the 3 `Privileged Gateway Intents`. Change the name again if you'd like. 


**Add it to your Discord**
- Under the `0auth --> URL Generator` tab, give it the `bot` scope, then in the newly displayed options list, select & enable `Send Messages`, `Manage Roles`, `Read Message History`, & `Read Messages/View Channels`. 

- Copy & Paste the generated link into your browser. Follow the prompts to add it to your server. 

**Roles**
- Create roles that match the names of your products. They don't have to match it exactly, just contain it. An example would be `VisAI - Framework`, `Verified Owner: VisAI - Framework`, etc. Whatever it is, it needs to match the names found in [config/config.ini](https://github.com/Visualistic-Studios/Unreal-Marketplace-Verification/blob/main/config/config.ini) `--> released_products`


**Channels**

The bot needs 3 channels to function: `Bot Interaction`, `Bot Interaction Testing`, and a `Bot Log`. Bot interaction is where users will request to be verified. The testing channel is for you to use for testing behind the scenes. Bot log is where the bot posts errors, any messages it gets, etc. 

- Create `Bot Interaction`, `Bot Interaction Testing`, and `Bot Log` channels (Names don't matter)
- Give the bot access to these channels (read & send)

## 6. Website
You'll need a privacy policy for customer data usage. Create one on your website, on GitHub, or another hosted location, and make sure to keep note of the link. 

## 7. Set the proper settings. 
