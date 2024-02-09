import telebot

from bot.handlers.callback_query import join_admin, remove_admin, join_user, remove_user, write_admin, write_user
from bot.handlers.message import start
from config import load_config
from module import user_manager

_description = '''
This bot allows you to receive and send anonymous messages for any joined user.
To do this you need to join with specifying your name.
Please, be polite with each other!

P.S.: No tracking, logging or saving any evidences of users activity.
'''


def register_handlers(bot: telebot.TeleBot):
    start.register_handlers(bot)
    join_admin.register_handlers(bot)
    remove_admin.register_handlers(bot)
    join_user.register_handlers(bot)
    remove_user.register_handlers(bot)
    write_admin.register_handlers(bot)
    write_user.register_handlers(bot)
    print('Handlers was registered')


if __name__ == '__main__':
    config = load_config()
    bot = telebot.TeleBot(config.tg_bot.token)

    user_manager.load_from_file()
    register_handlers(bot)

    bot.set_my_description(_description)
    bot.set_my_commands(
        commands=[telebot.types.BotCommand("/start", "Let's start from here!")],
        scope=telebot.types.BotCommandScopeAllPrivateChats())
    print('Bot was started...')
    bot.infinity_polling()
    print('Bot was stopped.')
