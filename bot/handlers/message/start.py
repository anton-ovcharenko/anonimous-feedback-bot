import os

from telebot import TeleBot
from telebot.types import Message

from bot import common

_welcome_message = f'''
 Welcome to {os.environ['BOT_NAME']}.
Join -> Wait for approval from admin-> Receive and write messages.
Use available actions below...
'''


def register_handlers(bot: TeleBot):
    bot.register_message_handler(start_handler, commands=['start', 'help'], pass_bot=True)


def start_handler(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    bot.send_message(chat_id, _welcome_message, reply_markup=common.build_keyboard(chat_id))
