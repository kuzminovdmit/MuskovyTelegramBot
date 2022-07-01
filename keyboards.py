from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


menu_btn = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(KeyboardButton('Огласите все города')).add(KeyboardButton('Хочу сам назвать город'))
