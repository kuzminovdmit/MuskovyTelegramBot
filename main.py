from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor

import logging
import handlers
import settings
import sys


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger('bot')

bot = Bot(token=settings.API_TOKEN)
dispatcher = Dispatcher(bot)

dispatcher.register_message_handler(handlers.start, commands=['start'])
dispatcher.register_message_handler(handlers.get_all_cities, lambda message: message.text == 'Огласите все города')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)