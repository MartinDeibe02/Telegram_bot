import logging
import os

#* Librerías externas
from dotenv import load_dotenv

#* Telegram
from telegram import Update, InputFile
from telegram.ext import (
    filters, 
    MessageHandler, 
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes,
    CallbackQueryHandler
)
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

#* Scripts de API
from utils.api_scripts.api_weather import *
from utils.api_scripts.api_nasa import *
from utils.api_scripts.api_jokes import *
from utils.api_scripts.api_bicicoruna import *

#* Scripts de scraping
from utils.scrap_scripts.leb_util import *
from utils.scrap_scripts.scrap_movies import *
from utils.scrap_scripts.scrap_news import *

#* Scripts de archivos
from utils.file_scripts.csv_json import *

#* Scripts de base de datos
from utils.bbdd_scripts.bd_query import *


os.environ['QT_QPA_PLATFORM'] = 'minimal'
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if BOT_TOKEN == None:
    print("Lembra indicar a variable TOKEN")
    print("p.ex: docker run --rm -e BOT_TOKEN=o_teu_token nomebot")
    exit(1)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = f"Bienvenido, {user['username']}!😁")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data :
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text = update.message.text)
    
    elif context.user_data['status'] == 'waiting_city':
        response = update.message.text
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text = get_api_weather(response))
        context.user_data['status'] = None

    elif context.user_data['status'] == 'waiting_bike':
        response = update.message.text
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text =  get_api_bicicoruna(response), parse_mode=ParseMode.MARKDOWN)
        context.user_data['status'] = None
    
    elif context.user_data['status'] == 'waiting_inf':
        response = update.message.text
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                       text =  get_inf_lvl(response), parse_mode=ParseMode.MARKDOWN)
        context.user_data['status'] = None


# * API            
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
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = description)

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
    
    
    
# * SCRAPING 
async def send_ladder_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Recuperando datos...", 
                                   parse_mode = ParseMode.MARKDOWN)
    image_buffer = leb_ladder()
    await context.bot.send_photo(chat_id = update.effective_chat.id, 
                                 caption = f"*🏀Clasificación LEBOro 2024🏀*", 
                                 photo = InputFile(image_buffer, 
                                 filename = 'ladder.png'), 
                                 parse_mode = ParseMode.MARKDOWN)

async def send_matches_table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_buffer = leb_results()
    await context.bot.send_photo(chat_id = update.effective_chat.id, 
                                 caption = f"*Partidos de la semana LEBOro 2024🏀*", 
                                 photo = InputFile(image_buffer, 
                                 filename = 'matches.png'), 
                                 parse_mode = ParseMode.MARKDOWN)
    
async def scrap_get_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    movie_list = get_movies()
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = movie_list, 
                                   parse_mode = ParseMode.MARKDOWN)
    
async def scrap_get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    news_list = get_news()
    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = news_list, 
                                   parse_mode = ParseMode.MARKDOWN)


# * FILE
async def converter(update, context):
    file = await context.bot.get_file(update.message.document)
    filename = update.message.document.file_name
    
    await file.download_to_drive(filename)
    current_directory = os.getcwd()
    ruta = f"{current_directory}/{filename}"
    
    if filename.endswith(".csv"):
        prueba = convert_file(ruta, 'csv_to_json')
        
        if prueba is None:
            
            await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Archivo no valido", 
                                   parse_mode = ParseMode.MARKDOWN)
            os.remove(ruta)

        else:
            
            await context.bot.send_document(update.effective_chat.id, document=prueba)
            info = str(info_file(ruta, 'csv'))
            await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = info, 
                                   parse_mode = ParseMode.MARKDOWN)
            os.remove(ruta)
            os.remove('data.json') 
        
    elif filename.endswith(".json"):
        prueba = convert_file(ruta, 'json_to_csv')

        if prueba is None:
            
            await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Archivo no valido", 
                                   parse_mode = ParseMode.MARKDOWN)
            os.remove(ruta)

        else:
            
            await context.bot.send_document(update.effective_chat.id, document=prueba)
            info = str(info_file(ruta, 'json'))
            await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = info, 
                                   parse_mode = ParseMode.MARKDOWN)
            os.remove(ruta)
            os.remove('data.csv') 
            
    else: 
        
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Archivo no valido", 
                                   parse_mode = ParseMode.MARKDOWN)
        os.remove(ruta)

# * DATABASE
async def get_inferno(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    context.user_data['status'] = 'waiting_inf'

    await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Introduce un nombre para comrobar si esta en el infierno", 
                                   parse_mode = ParseMode.MARKDOWN)


# * BOTONES
async def leb_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Clasificación", callback_data='ladder'),
        InlineKeyboardButton("Partidos", callback_data='matches')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                  text="🏀 Que quieres consultar?:",
                                  reply_markup=reply_markup)
    
async def bicicoruna_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Consultar parada", callback_data='consult'),
        InlineKeyboardButton("Listar paradas", callback_data='list')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                  text="🚲 Que quieres consultar?:",
                                  reply_markup=reply_markup)

async def on_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'ladder':
        await send_ladder_table(update, context)
    elif query.data == 'matches':
        await send_matches_table(update, context)
    elif query.data == 'consult':
        await get_bicicoruna(update, context)
    elif query.data == 'list':
        await get_list_bikes(update, context)



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
    
    joke_handler = CommandHandler('broma', get_joke)
    application.add_handler(joke_handler)
    
    cartelera_handler = CommandHandler('cartelera', scrap_get_movies)
    application.add_handler(cartelera_handler)
    
    news_handler = CommandHandler('noticias', scrap_get_news)
    application.add_handler(news_handler)
    
    inf_handler = CommandHandler('infierno', get_inferno)
    application.add_handler(inf_handler)
    
    leb_options_handler = CommandHandler('leb', leb_options)
    application.add_handler(leb_options_handler)
    
    bicicoruna_options_handler = CommandHandler('bicicoruna', bicicoruna_options)
    application.add_handler(bicicoruna_options_handler)
    
    callback_query_handler = CallbackQueryHandler(on_callback_query)
    application.add_handler(callback_query_handler)
    
    application.add_handler(MessageHandler(filters.Document.ALL, converter))
    application.run_polling()
