import telebot

from bot.handlers.callback_query import join_admin, remove_admin, join_user, remove_user, write_admin, write_user
from bot.handlers.message import start
from config import *
from module import user_manager

_description = '''
This bot allows you to receive and send anonymous messages for any joined user.
To do this you need to join with specifying your name.
Please, be polite with each other!

P.S.: No tracking, logging or saving any evidences of users activity.
'''

# if "TELEBOT_BOT_TOKEN" not in os.environ or "GROUP_CHAT_ID" not in os.environ:
#     raise AssertionError("Please configure TELEBOT_BOT_TOKEN and GROUP_CHAT_ID as environment variables")
#
# bot = telebot.AsyncTeleBot(os.environ["TELEBOT_BOT_TOKEN"])
# GROUP_CHAT_ID = int(os.environ["GROUP_CHAT_ID"])


bot = telebot.TeleBot(BOT_TOKEN)


def register_handlers():
    start.register_handlers(bot)
    join_admin.register_handlers(bot)
    remove_admin.register_handlers(bot)
    join_user.register_handlers(bot)
    remove_user.register_handlers(bot)
    write_admin.register_handlers(bot)
    write_user.register_handlers(bot)


if __name__ == '__main__':
    user_manager.load_from_file()
    register_handlers()

    bot.set_my_description(_description)
    bot.set_my_commands(
        commands=[telebot.types.BotCommand("/start", "Let's start from here!")],
        scope=telebot.types.BotCommandScopeAllPrivateChats())
    bot.infinity_polling()
