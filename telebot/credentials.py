import os

bot_token = ""
bot_user_name = ""
URL = ""

if "BOT_TOKEN" in os.environ:
    bot_token = os.environ['BOT_TOKEN']

if "BOT_USERNAME" in os.environ:
    bot_user_name = os.environ['BOT_USERNAME']

if "URL" in os.environ:
    URL = os.environ['URL']