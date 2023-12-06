import telebot

from bot.handlers import callback_query

_callback_data_delimiter = '~'


def get_callback_data_delimiter():
    return _callback_data_delimiter


def build_callback_data(*args):
    return _callback_data_delimiter.join(map(str, args))


def build_keyboard(chat_id: int):
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_query.join_admin.fill_keyboard(keyboard)
    callback_query.remove_admin.fill_keyboard(keyboard, chat_id)
    callback_query.join_user.fill_keyboard(keyboard, chat_id)
    callback_query.remove_user.fill_keyboard(keyboard, chat_id)
    callback_query.write_admin.fill_keyboard(keyboard)
    callback_query.write_user.fill_keyboard(keyboard, chat_id)
    return keyboard
