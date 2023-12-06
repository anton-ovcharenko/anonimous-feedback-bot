from telebot import TeleBot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import common
from module import user_manager


def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(
        select_user_handler,
        func=lambda call: call.data == 'select_user',
        pass_bot=True)
    bot.register_callback_query_handler(
        write_user_handler,
        func=lambda call: call.data.startswith(f'write_user{common.get_callback_data_delimiter()}'),
        pass_bot=True)


def fill_keyboard(keyboard: InlineKeyboardMarkup, chat_id: int):
    if user_manager.is_user_exist(chat_id):
        keyboard.add(InlineKeyboardButton(text="Send message", callback_data='select_user'))


def select_user_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    keyboard = common.build_keyboard(chat_id)
    if not user_manager.is_user_exist(chat_id):
        msg = f'You are not joined yet'
    elif len(user_manager.get_users()) == 1:
        msg = f'There are no other users yet'
    else:
        keyboard = InlineKeyboardMarkup()
        msg = f'Select someone to send message:'
        for client_chat_id, user in user_manager.get_users().items():
            if client_chat_id == chat_id:
                continue
            keyboard.row(
                InlineKeyboardButton(text=user['name'], callback_data=common.build_callback_data('write_user',
                                                                                                 client_chat_id,
                                                                                                 user['name'])))
    bot.send_message(chat_id, msg, reply_markup=keyboard)
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)


def write_user_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    data_parts = call.data.split(common.get_callback_data_delimiter())
    bot.send_message(chat_id, f'Enter your message for {data_parts[2]}:')
    bot.register_next_step_handler(call.message, send_message, bot, int(data_parts[1]))
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)


def send_message(message: Message, bot: TeleBot, recipient_chat_id: int):
    sender_chat_id = message.chat.id
    bot.send_message(sender_chat_id, f'Your message was sent', reply_markup=common.build_keyboard(sender_chat_id))
    # todo add rephrase mechanism
    bot.send_message(recipient_chat_id, f'Anonym >> {message.text}')
