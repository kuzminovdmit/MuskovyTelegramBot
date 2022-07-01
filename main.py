import logging
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import handlers
import settings


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger('bot')

bot = Bot(token=settings.API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

dispatcher.register_message_handler(
    handlers.start,
    commands=['start'],
    state='*'
)
dispatcher.register_message_handler(
    handlers.await_query,
    lambda message: message.text in ['Поиск по названию', 'Искать ещё'],
    state=handlers.GetCity.waiting_for_query
)
dispatcher.register_message_handler(
    handlers.get_similar_names,
    state=handlers.GetCity.waiting_for_search
)
dispatcher.register_message_handler(
    handlers.get_city_data,
    state=handlers.GetCity.waiting_for_choice
)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
