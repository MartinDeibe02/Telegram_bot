import logging
import os
os.environ['QT_QPA_PLATFORM'] = 'minimal'
from dotenv import load_dotenv

from telegram import Update, InputFile
from telegram.ext import Updater, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode

from utils.api_scripts.api_weather import *
from utils.api_scripts.api_nasa import *
from utils.api_scripts.api_jokes import *
from utils.api_scripts.api_bicicoruna import *


from utils.scrap_scripts.leb_util import *
from utils.scrap_scripts.scrap_movies import *
from utils.scrap_scripts.scrap_news import *
from utils.file_scripts.csv_json import *

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


async def file_test(update, context):
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
            os.remove(ruta)
            os.remove('data.csv') 
            
    else: 
        
        await context.bot.send_message(chat_id = update.effective_chat.id, 
                                   text = "Archivo no valido", 
                                   parse_mode = ParseMode.MARKDOWN)
        os.remove(ruta)



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
    
    news_handler = CommandHandler('noticias', scrap_get_news)
    application.add_handler(news_handler)
    
    
    application.add_handler(MessageHandler(filters.Document.ALL, file_test))
    application.run_polling()
