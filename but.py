from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from sqlight import all_by_user


def til():
    mrk = InlineKeyboardMarkup(row_width=2)
    bt = InlineKeyboardButton('Уз 🇺🇿', callback_data='uz')
    btn = InlineKeyboardButton('Ру 🇷🇺', callback_data='ru')
    mrk.add(bt, btn)
    return mrk


def mainkeys(lang):
    mrk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == "uz":
        btn1 = KeyboardButton('❇️ Умумий маълумотлар')
        btn2 = KeyboardButton('🆕 Янги ID қўшиш')
        btn3 = KeyboardButton('🗑❌ ID ни ўчириш')
        btn4 = KeyboardButton('💴 Умумий баланс')
        btn5 = KeyboardButton('♻️ Тилни ўзгартириш')
        btn6 = KeyboardButton('🔙 Ортга')
    else:
        btn1 = KeyboardButton('❇️ Общие данные')
        btn2 = KeyboardButton('🆕 Добавить новый идентификатор')
        btn3 = KeyboardButton('🗑❌ Удалить идентификатор')
        btn4 = KeyboardButton('💴 Общий баланс')
        btn5 = KeyboardButton('♻️ Изменить язык')
        btn6 = KeyboardButton('🔙 Назад')

    mrk.add(btn5, btn4, btn1, btn2, btn6, btn3)
    return mrk


async def all_keyboard(user_id):
    requests = all_by_user(user_id)
    if requests:
        inline_keyboard = []
        for i in requests:
            inline_keyboard.append([InlineKeyboardButton(text=i[2], callback_data=i[0])])
        markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return markup
    else:
        return None


def back_main(lang):
    mrk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == "uz":
        btn1 = KeyboardButton('◀️Орқага')
    else:
        btn1 = KeyboardButton('◀️Назад')

    mrk.add(btn1)
    return mrk
