from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import common
from module import user_manager


def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(join_admin_handler,
                                        func=lambda call: call.data == 'join_admin',
                                        pass_bot=True)


def fill_keyboard(keyboard: InlineKeyboardMarkup):
    if not user_manager.is_admin_set():
        keyboard.add(InlineKeyboardButton(text="Join as admin", callback_data='join_admin'))


def join_admin_handler(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    if user_manager.is_admin_set():
        msg = f'Admin role is already defined'
    else:
        user_manager.add_admin(chat_id)
        msg = f'You were successfully promoted to admin'
    bot.send_message(chat_id, msg, reply_markup=common.build_keyboard(chat_id))
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)
