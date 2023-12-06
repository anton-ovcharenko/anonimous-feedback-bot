import re

from telebot import TeleBot
from telebot.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot import common
from module import user_manager


def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(
        join_user_handler,
        func=lambda call: call.data == 'join_user',
        pass_bot=True)
    bot.register_callback_query_handler(
        join_user_decline_handler,
        func=lambda call: call.data.startswith(f'join_user_decline{common.get_callback_data_delimiter()}'),
        pass_bot=True)
    bot.register_callback_query_handler(
        join_user_approve_handler,
        func=lambda call: call.data.startswith(f'join_user_approve{common.get_callback_data_delimiter()}'),
        pass_bot=True)


def fill_keyboard(keyboard: InlineKeyboardMarkup, chat_id: int):
    if not user_manager.is_user_exist(chat_id):
        keyboard.add(InlineKeyboardButton(text="Join", callback_data='join_user'))


def join_user_handler(call: CallbackQuery, bot: TeleBot):
    message = call.message
    request_user_name(message, bot)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=None)


def request_user_name(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    if user_manager.is_user_exist(chat_id):
        msg = f'You are already joined'
    else:
        user_manager.add_admin(chat_id)
        msg = f'Enter your name (only latin letters and space are allowed):'
        bot.register_next_step_handler(message, join_user_request_handler, bot)
    bot.send_message(chat_id, msg)


def join_user_request_handler(message: Message, bot: TeleBot):
    client_chat = message.chat
    client_name = message.text
    if not re.compile(r'^[a-zA-Z\s]+$').match(client_name):
        bot.send_message(client_chat.id, f'Name has invalid format, try again.')
        request_user_name(message, bot)
    else:
        for admin_chat_id in user_manager.get_administrators():
            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton(text="Approve",
                                     callback_data=common.build_callback_data('join_user_approve',
                                                                              client_chat.id,
                                                                              client_name,
                                                                              client_chat.username)))
            keyboard.add(
                InlineKeyboardButton(text="Decline",
                                     callback_data=common.build_callback_data('join_user_decline',
                                                                              client_chat.id)))
            bot.send_message(admin_chat_id,
                             f'New join request from: {client_name} ({client_chat.username}/{client_chat.id})',
                             reply_markup=keyboard)
        bot.send_message(client_chat.id,
                         f'Your join request was sent to admin. You will get notification after approval')


def join_user_approve_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    data_parts = call.data.split(common.get_callback_data_delimiter())
    client_chat_id = data_parts[1]
    user_manager.add_user(int(client_chat_id), data_parts[2], data_parts[3])
    bot.send_message(client_chat_id, f'Your join request was approved', reply_markup=common.build_keyboard(chat_id))
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)


def join_user_decline_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    client_chat_id = call.data.split(common.get_callback_data_delimiter())[1]
    bot.send_message(client_chat_id, f'Your join request was declined', reply_markup=common.build_keyboard(chat_id))
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)
