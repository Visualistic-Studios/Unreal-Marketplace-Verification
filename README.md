# Unreal Engine Marketplace Verification

Project that enables the automation of Unreal Engine product verification using a Discord bot. 

# TEMPORARY NOTE:

- Currently the project works, but isn't updated with a complete guide just yet. It also needs some work. I would love to make this a more reliable, secure, and complete solution. If you find yourself wanting to help, [join the Discord](https://discord.gg/FEnDUZ7rNK) & send me a message!


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
It is recommended to create a new Gmail account specifically for the purpose of verifying your users. Don't sign up for anything using this account; keep it specific for this purpose. Give it a very strong, high entropy password.

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
