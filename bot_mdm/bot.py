import logging
import os
from telegram import Update
from telegram.ext import Updater, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackContext
from dotenv import load_dotenv
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

from utils.api_scripts.api_weather import *

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data['status'] != None:
        response = update.message.text

        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_weather(response))
        context.user_data['status'] = None

    else: 
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def get_Weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['status'] = 'waiting_city'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="De que ciudad quieres saber el tiempo?")


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    
    weather_handler = CommandHandler('prueba', get_Weather)
    application.add_handler(weather_handler)
    
    application.run_polling()
