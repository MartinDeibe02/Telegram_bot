import logging
import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackContext
from telegram.constants import ParseMode

from utils.api_scripts.api_weather import *
from utils.api_scripts.api_nasa import *
from utils.api_scripts.api_jokes import *
from utils.api_scripts.api_bicicoruna import *

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Binvenido, {user['username']}!😁")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data['status'] == 'waiting_city':
        response = update.message.text

        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_api_weather(response))
        context.user_data['status'] = None

    elif context.user_data['status'] == 'waiting_bike':
        response = update.message.text

        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_api_bicicoruna(response), parse_mode=ParseMode.MARKDOWN)
        context.user_data['status'] = None
        
    else: 
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def get_Weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = 'waiting_city'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="De que ciudad quieres saber el tiempo?")

async def get_apod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title, description, url = get_api_apod()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=f"{title}", parse_mode=ParseMode.MARKDOWN)

async def get_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_api_joke())

async def get_bicicoruna(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    context.user_data['status'] = 'waiting_bike'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Introduce el nombre de una estacion de bicicoruna")

async def get_list_bikes(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=list_stations(), parse_mode=ParseMode.MARKDOWN))
    
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    weather_handler = CommandHandler('tiempo', get_Weather)
    application.add_handler(weather_handler)
    
    apod_handler = CommandHandler('apod', get_apod)
    application.add_handler(apod_handler)
    
    joke_handler = CommandHandler('joke', get_joke)
    application.add_handler(joke_handler)
    
    bicicoruna_handler = CommandHandler('bicicoruna', get_bicicoruna)
    application.add_handler(bicicoruna_handler)
    
    bike_list_handler = CommandHandler('lista', get_list_bikes)
    application.add_handler(bike_list_handler)
    
    application.run_polling()
