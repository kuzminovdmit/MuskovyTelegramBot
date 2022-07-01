from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

import db
import parser


class GetCity(StatesGroup):
    waiting_for_query = State()
    waiting_for_search = State()
    waiting_for_choice = State()


async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(text='Поиск по названию'))

    await message.reply(
        'Приветствую, я знаю все города в Московской области и могу поделиться ссылкой на их страницу в википедии.',
        reply_markup=keyboard
    )

    cities = await parser.parser()
    conn = await db.connect_to_db()

    if not await db.is_table_exists(conn):
        await db.create_table(conn)
    else:
        await db.truncate_table(conn)

    await db.populate_table(conn, cities)

    await conn.close()

    await GetCity.next()


async def await_query(message: types.Message):
    await message.answer('Пиши название города, я жду')

    await GetCity.next()


async def get_similar_names(message: types.Message):
    conn = await db.connect_to_db()
    found_cities = await db.search(conn, message.text)

    if found_cities:
        cities_list = [city['name'] for city in found_cities]

        await GetCity.next()

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for city_name in cities_list:
            keyboard.add(types.KeyboardButton(city_name))

        await message.answer(f'Вот что я нашел по запросу {message.text}', reply_markup=keyboard)
    else:
        await GetCity.waiting_for_query.set()

        await message.answer(f'Я ничего не нашел по запросу {message.text}')

    await conn.close()


async def get_city_data(message: types.Message):
    conn = await db.connect_to_db()

    city_data = await db.retrieve(conn, message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Искать ещё'))

    await message.answer(
        f"Город {city_data['name'].rstrip()} с населением {city_data['population']} человек в <a href='{city_data['link']}'>википедии</a>",
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await conn.close()

    await GetCity.waiting_for_query.set()
