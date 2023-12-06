from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import common
from module import user_manager


def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(remove_admin_handler,
                                        func=lambda call: call.data == 'remove_admin',
                                        pass_bot=True)


def fill_keyboard(keyboard: InlineKeyboardMarkup, chat_id: int):
    if user_manager.is_admin_exist(chat_id):
        keyboard.add(InlineKeyboardButton(text="Remove yourself from admins", callback_data='remove_admin'))


def remove_admin_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    user_manager.remove_admin(chat_id)
    bot.send_message(chat_id,
                     'You was removed from admin list.',
                     reply_markup=common.build_keyboard(chat_id))
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)
