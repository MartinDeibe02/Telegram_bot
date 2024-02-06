import logging
import os
os.environ['QT_QPA_PLATFORM'] = 'minimal'

from dotenv import load_dotenv
import time

from telegram import Update, InputFile
from telegram.ext import Updater, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackContext
from telegram.constants import ParseMode

from utils.api_scripts.api_weather import *
from utils.api_scripts.api_nasa import *
from utils.api_scripts.api_jokes import *
from utils.api_scripts.api_bicicoruna import *


from utils.scrap_scripts.leb_util import *
from utils.scrap_scripts.scrap_movies import *

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = f"Binvenido, {user['username']}!😁")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data['status'] == 'waiting_city':
        response = update.message.text
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text = get_api_weather(response))
        context.user_data['status'] = None

    elif context.user_data['status'] == 'waiting_bike':
        response = update.message.text
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text =  get_api_bicicoruna(response), parse_mode=ParseMode.MARKDOWN)
        context.user_data['status'] = None
        
    else: 
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text = update.message.text)


async def get_Weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = 'waiting_city'
    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text = "De que ciudad quieres saber el tiempo?")

async def get_apod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title, description, url = get_api_apod()
    await context.bot.send_photo(chat_id = update.effective_chat.id, 
                                 photo = url, 
                                 caption = f"{title}", 
                                 parse_mode = ParseMode.MARKDOWN)

async def get_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = get_api_joke())

async def get_bicicoruna(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    context.user_data['status'] = 'waiting_bike'
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Introduce el nombre de una estacion de bicicoruna")

async def get_list_bikes(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = list_stations(), 
                                   parse_mode = ParseMode.MARKDOWN)
    
    
async def send_ladder_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_buffer = leb_ladder()
    await context.bot.send_photo(chat_id = update.effective_chat.id, 
                                 caption = f"*🏀Clasificación LEBOro 2024🏀*", 
                                 photo = InputFile(image_buffer, 
                                 filename = 'ladder.png'), 
                                 parse_mode = ParseMode.MARKDOWN)


async def send_matches_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_buffer = leb_results()
    await context.bot.send_photo(chat_id = update.effective_chat.id, 
                                 caption = f"*Últimos partidos LEBOro 2024🏀*", 
                                 photo = InputFile(image_buffer, 
                                 filename = 'matches.png'), 
                                 parse_mode = ParseMode.MARKDOWN)
    
async def scrap_get_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    movie_list = get_movies()
    print(movie_list)
    


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

    leb_ladder_handler = CommandHandler('clasificacion', send_ladder_table)
    application.add_handler(leb_ladder_handler)
    
    leb_matches_handler = CommandHandler('partidos', send_matches_table)
    application.add_handler(leb_matches_handler)
    
    cartelera_handler = CommandHandler('cartelera', scrap_get_movies)
    application.add_handler(cartelera_handler)
    
    application.run_polling()
