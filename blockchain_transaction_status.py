import logging
import requests
import pytz
from datetime import datetime, timedelta
from dateutil import parser
from telegram import Update
from telegram.ext import *

TOKEN = 'YOUR TOKEN'

BASE_URL = "https://api.blockcypher.com/v1/btc/main"
REDIRECT_BASE_URL = "https://live.blockcypher.com/btc"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey! Give me a BTC hash id and I'll give you the"
                                                                    " confirmation count.\nUse the command"
                                                                    " /check_confirmations 'your_hash'."
                                                                    "\neg: /check_confirmations foobar$#@123")


def check_confirmations(update: Update, context: CallbackContext):
    tx_hash = context.args[0]
    response = requests.get(f"{BASE_URL}/txs/{tx_hash}")

    if response.status_code == 200:
        response_json = response.json()
        if response_json['confirmations'] >= 6:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Transaction 100% successful")
        else:
            received_time = parser.parse(response_json['received']).replace(tzinfo=pytz.FixedOffset(-330))
            received_time = received_time.astimezone(pytz.timezone('UTC'))
            received_time = received_time.replace(tzinfo=None)
            current_time = datetime.now()
            time_difference = current_time - received_time
            if time_difference < timedelta(minutes=1):
                time_ago = "Just now"
            elif time_difference < timedelta(hours=1):
                time_ago = f"{time_difference.seconds // 60} minutes ago"
            elif time_difference < timedelta(days=1):
                time_ago = f"{time_difference.seconds // 3600} hours ago"
            else:
                time_ago = f"{time_difference.days} days ago"
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Confirmations: {response_json['confirmations']}"
                                          f"\nAmount transacted in BTC: {response_json['total'] * pow(10, -8):.20f}"
                                          f"\nFees: {response_json['fees'] * pow(10, -8)}"
                                          f"\nReceived {time_ago}"
                                          f"\nCheck the status on "
                                          f"{REDIRECT_BASE_URL}/tx/{tx_hash}/")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"An error occurred: {response.text}.  Please enter a valid hash")


start_handler = CommandHandler('start', start)
check_confirmations = CommandHandler('check_confirmations', check_confirmations)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(check_confirmations)

updater.start_polling()

