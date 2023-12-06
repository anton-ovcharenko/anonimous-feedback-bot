from telebot import TeleBot
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import common
from module import user_manager


def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(write_admin_handler,
                                        func=lambda call: call.data == 'write_admin',
                                        pass_bot=True)


def fill_keyboard(keyboard: InlineKeyboardMarkup):
    if user_manager.is_admin_set():
        keyboard.add(InlineKeyboardButton(text="Write to admin", callback_data='write_admin'))


def write_admin_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Enter your message for admin:')
    bot.register_next_step_handler(call.message, send_admin, bot)
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)


def send_admin(message: Message, bot: TeleBot):
    client_chat = message.chat
    for admin_chat_id in user_manager.get_administrators():
        msg = "New message from {0} {1} ({2}/{3}): {4}".format(client_chat.first_name,
                                                               client_chat.last_name,
                                                               client_chat.username,
                                                               client_chat.id,
                                                               message.text)
        bot.send_message(admin_chat_id, msg)
    bot.send_message(client_chat.id, 'Your message was sent', reply_markup=common.build_keyboard(client_chat.id))
