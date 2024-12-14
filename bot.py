from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

# Flask app
app = Flask(__name__)

# Telegram Bot API token
BOT_TOKEN = "7718816702:AAHox0wPDUa_cp-l_m2WxVnIgSJ-x-hfkhw"
CHANNEL_ID = "@plxbd_official"  # Your channel username or ID

# Telegram bot instance
bot = Bot(token=BOT_TOKEN)

# Webhook route for Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return "ok", 200

# Function to search and send movies
def search_movie(update, context):
    query = update.message.text
    found = False

    # Search for the query in the channel
    for message in bot.get_chat(CHANNEL_ID).history():
        if query.lower() in (message.caption or "").lower():
            bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=CHANNEL_ID, message_id=message.message_id)
            found = True
            break

    if not found:
        update.message.reply_text("Sorry, I couldn't find the movie you're looking for.")

# Setup dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search_movie))

# Home route for health check
@app.route('/')
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run()
