import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
import json
from telebot import chatfunctions

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
 
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    print(update)

    chat_id = ""
    msg_id = ""
    text = ""

    boolIsEditedMessage = False
    boolIsNewGroup = False
    boolIsCallbackQuery = False
    if update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
        boolIsCallbackQuery = True
    elif update.edited_message.chat.type == 'group' and update.message.text is None:
        chat_id = update.edited_message.chat.id
        msg_id = update.edited_message.message_id
        text = update.edited_message.text.encode('utf-8').decode()
        boolIsEditedMessage = True
    elif update.message.chat.type == 'group' and update.message.text is None:
        chat_id = update.message.chat_id
        boolIsNewGroup = True
    elif update.message is None:
        chat_id = update.edited_message.chat.id
        msg_id = update.edited_message.message_id
        text = update.edited_message.text.encode('utf-8').decode()
        boolIsEditedMessage = True
    else:
        chat_id = update.message.chat.id
        msg_id = update.message.message_id
        text = update.message.text.encode('utf-8').decode()

    # Telegram understands UTF-8, so encode text for unicode compatibility
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
        Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
        """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome)

    elif boolIsNewGroup:
        bot.sendMessage(chat_id=chat_id, text="I am Rocketing")
    
    elif boolIsCallbackQuery:
        bot.sendMessage(chat_id=chat_id, text="We don't do callbacks")

    elif "/getquote" in text:
        replyText, keyboardMarkup = chatfunctions.displayQuote(text)
        if keyboardMarkup is not None:
            bot.sendMessage(chat_id=chat_id, text=replyText, reply_to_message_id=msg_id, parse_mode=telegram.ParseMode.MARKDOWN_V2, reply_markup=keyboardMarkup)
        else:
            bot.sendMessage(chat_id=chat_id, text=replyText, reply_to_message_id=msg_id)

    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"W", "_", text)
            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            bot.sendPhoto(chat_id=chat_id, photo=url) # , reply_to_message_id=msg_id
        except Exception:
            # if things went wrong
            # bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name")
            pass

    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)