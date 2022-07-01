from aiogram import types

import db
import keyboards


async def start(message: types.Message):
    await message.reply('''
Приветствую, я знаю все города в Московской области и могу поделиться ссылкой на их страницу в википедии.
        
Напиши мне какой-нибудь город или попроси меня огласить весь список.
    ''', reply_markup=keyboards.menu_btn)


async def get_all_cities(message: types.Message):
    cities_data = await db.get_all_cities_name()
    await message.answer('Городов в Подмосковье полно, в одно сообщение не поместятся:')
    await message.answer(cities_data[0])
    await message.answer(cities_data[1])
