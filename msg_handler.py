from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
import requests
from aiogram import types
from bot_token import dp, bot
from aiogram.dispatcher.filters.builtin import CommandStart
from sqlight import register_user, gg, register_request, get_summa, delete_request, users_id
from but import *
from aiogram.types import ReplyKeyboardRemove


@dp.channel_post_handler(state='*')
async def for_message(message: types.Message):
    message_id = message.message_id
    users = users_id()
    for user in users:
        await bot.forward_message(from_chat_id='-1001430995089', chat_id=user, message_id=message_id)


@dp.message_handler(CommandStart(), state='*')
async def start_Go(msg: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=msg.chat.id, text=f'Ассалому алайкум {msg.chat.full_name} 👋\n\"BB Logistics\"нинг '
                                                     f'расмий ботига хуш келибсиз 🚛\nИлтимос тилни танланг 👇🏻\n\nЗдраствуйте уважаемый {msg.chat.full_name} 👋\nДобро пожаловать на официальный бот \"BB Logistics\" 🚛\nПожалуйста выберите язык 👇🏻',
                           reply_markup=til())


@dp.message_handler(lambda message: message.text in ['🔙 Ортга', '🔙 Назад'], state='*')
async def go_main(message: Message, state: FSMContext):
    await state.finish()
    if message.text == '🔙 Ortga':
        await bot.send_message(chat_id=message.chat.id, text='Сиз ортга қайтдингиз', reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(chat_id=message.chat.id, text='Вы вернулись назад', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Ассалому алайкум {message.chat.full_name} 👋\n\"BB Logistics\"нинг '
                                f'расмий ботига хуш келибсиз 🚛\nИлтимос тилни танланг 👇🏻\n\nЗдраствуйте уважаемый {message.chat.full_name} 👋\nДобро пожаловать на официальный бот \"BB Logistics\" 🚛\nПожалуйста выберите язык 👇🏻',
                           reply_markup=til())


@dp.message_handler(lambda message: message.text in ['◀️Орқага', '◀️Назад'], state='*')
async def go_main(message: Message, state: FSMContext):
    if gg(message.chat.id)[0] == 'uz':
        await bot.send_message(chat_id=message.chat.id, text='👤 Шахсий кабинет', parse_mode='HTML',
                               reply_markup=mainkeys(gg(message.chat.id)[0]))
        await state.set_state('get_com')
    else:
        await bot.send_message(chat_id=message.chat.id, text='👤 Личный кабинет', parse_mode='HTML',
                               reply_markup=mainkeys(gg(message.chat.id)[0]))
        await state.set_state('get_com')


@dp.callback_query_handler(lambda call: call.data in ['uz', 'ru'])
async def til_tanlash(call: CallbackQuery, state: FSMContext):
    register_user(user=call.from_user.id, lang=call.data, ism=call.from_user.first_name)
    if call.data == 'uz':
        text = 'Сиз Узбек 🇺🇿 тилини танладингиз. Маълумот олиш учун илтимос етказиш ID рақамини киритинг ✏'
    else:
        text = 'Вы выбрали Русский язык 🇷🇺. Вводите ID перевозки  чтобы получать данные ✏'
    await state.set_state('main')
    await bot.edit_message_text(chat_id=call.from_user.id, text=text, message_id=call.message.message_id)


@dp.message_handler(state='main')
async def main(message: Message, state: FSMContext):
    req_id = message.text
    if not req_id.isdigit():
        if gg(message.chat.id)[0] == 'uz':
            await message.answer(text='Бундай етказиш ID si мавжуд эмас ❌', parse_mode='HTML')
        else:
            await message.answer(text='Не сущеуствует c таким ID перевозки ❌', parse_mode='HTML')
        await state.set_state("main")
    else:
        await state.finish()
        ship_id = ''
        cost = ''
        url = 'http://185.65.202.117:7979/leads/'
        try:
            resp = requests.get(url + req_id)
            a = resp.json()
            if a.get('id'):
                cost = a.get('price')
                a = a.get('custom_fields_values')
                for i in a:
                    if i.get('field_name') == 'Перевозка':
                        ship_id = i.get('values')[0].get('value')
                register_request(user_id=message.chat.id, req_id=req_id, ship_id=ship_id, cost=cost)
                if gg(message.chat.id)[0] == 'uz':
                    await bot.send_message(chat_id=message.chat.id, text='👤 Шахсий кабинет', parse_mode='HTML',
                                           reply_markup=mainkeys(gg(message.chat.id)[0]))
                    await state.set_state('get_com')
                else:
                    await bot.send_message(chat_id=message.chat.id, text='👤 Личный кабинет', parse_mode='HTML',
                                           reply_markup=mainkeys(gg(message.chat.id)[0]))
                    await state.set_state('get_com')
            else:
                if gg(message.chat.id)[0] == 'uz':
                    await message.answer(text='Бундай етказиш ID si мавжуд эмас ❌', parse_mode='HTML')
                else:
                    await bot.edit_message_text(text='Не сущеуствует c таким ID перевозки ❌', parse_mode='HTML')
                await state.set_state('main')
        except Exception as exxx:
            print(exxx)
            if gg(message.chat.id)[0] == 'uz':
                await message.answer(text='Бундай етказиш ID si мавжуд эмас ❌', parse_mode='HTML')
            else:
                await bot.edit_message_text(text='Не сущеуствует c таким ID перевозки ❌', parse_mode='HTML')
            await state.set_state("main")


@dp.message_handler(state='get_com')
async def get_command(message: Message, state: FSMContext):
    com = message.text
    if com == '❇️ Умумий маълумотлар' or com == '❇️ Общие данные':
        markup = await all_keyboard(message.from_user.id)
        if markup is not None:
            lang = gg(message.chat.id)[0]
            if lang == 'uz':
                await bot.send_message(chat_id=message.from_user.id, text='❇️ Умумий маълумотлар бўлими',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id, text="Керакли ID ни танланг 👇",
                                       reply_markup=markup)
            else:
                await bot.send_message(chat_id=message.from_user.id, text='❇️ Раздел общей информации',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный ID 👇",
                                       reply_markup=markup)
            await state.set_state('get_info')
        else:
            lang = gg(message.chat.id)[0]
            if lang == 'uz':
                await bot.send_message(chat_id=message.from_user.id, text="Рўйхат бўш. Янги ID ни киритинг 👇",
                                       reply_markup=back_main(lang))
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Список пуст. Введите новый идентификатор 👇",
                                       reply_markup=back_main(lang))
            await state.set_state('main')
    if com == '🗑❌ ID ни ўчириш' or com == '🗑❌ Удалить идентификатор':
        lang = gg(message.chat.id)[0]
        markup = await all_keyboard(message.from_user.id)
        if markup is not None:
            if lang == 'uz':
                await bot.send_message(chat_id=message.from_user.id, text='🗑 ID ни ўчириш бўлими',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id, text="Керакли ID ни танланг 👇",
                                       reply_markup=markup)
            else:
                await bot.send_message(chat_id=message.from_user.id, text='🗑 Pаздел yдалить идентификатора',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный ID 👇",
                                       reply_markup=markup)
            await state.set_state('delete_request')
        else:
            lang = gg(message.chat.id)[0]
            if lang == 'uz':
                await bot.send_message(chat_id=message.from_user.id, text="Рўйхат бўш. Янги ID ни киритинг 👇",
                                       reply_markup=back_main(lang))
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Список пуст. Введите новый идентификатор 👇",
                                       reply_markup=back_main(lang))
            await state.set_state('main')
    elif com == '🆕 Янги ID қўшиш' or com == '🆕 Добавить новый идентификатор':
        lang = gg(message.chat.id)[0]
        if lang == 'uz':
            await bot.send_message(chat_id=message.from_user.id, text="Yangi ID ni kiriting 👇",
                                   reply_markup=back_main(lang))
        else:
            await bot.send_message(chat_id=message.from_user.id, text="Введите новый идентификатор 👇",
                                   reply_markup=back_main(lang))
        await state.set_state('main')
    elif com == '♻️ Изменить язык' or com == '♻️ Тилни ўзгартириш':
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Илтимос тилни танланг 👇🏻\n\nПожалуйста выберите язык 👇🏻',
                               reply_markup=til())
        await state.set_state('change_lang')
    elif com == '💴 Общий баланс' or com == '💴 Умумий баланс':
        # summa = get_summa(message.from_user.id)
        # lang = gg(message.chat.id)[0]
        # if lang == 'uz':
        #     await bot.send_message(chat_id=message.from_user.id, text=f"💴 Умумий баланс: ${summa}")
        # else:
        #     await bot.send_message(chat_id=message.from_user.id, text=f"💴 Общий баланс: ${summa}")
        # await state.set_state('get_com')
        markup = await all_keyboard(message.from_user.id)
        if markup is not None:
            lang = gg(message.chat.id)[0]
            if lang == 'uz':
                await bot.send_message(chat_id=message.from_user.id, text='💴 Умумий баланслар бўлими',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id, text="Керакли ID ни танланг 👇",
                                       reply_markup=markup)
            else:
                await bot.send_message(chat_id=message.from_user.id, text='💴 Раздел  общих балансов',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный ID 👇",
                                       reply_markup=markup)
            await state.set_state('get_finance')
        else:
            lang = gg(message.chat.id)[0]
            if lang == 'uz':
                await bot.send_message(chat_id=message.from_user.id, text="Рўйхат бўш. Янги ID ни киритинг 👇",
                                       reply_markup=back_main(lang))
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Список пуст. Введите новый идентификатор 👇",
                                       reply_markup=back_main(lang))
            await state.set_state('main')
    elif com == '🔙 Назад' or com == '🔙 Ортга':
        await state.finish()
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Ассалому алайкум {message.chat.full_name} 👋\n\"BB Logistics\"нинг '
                                    'расмий ботига хуш келибсиз 🚛\nИлтимос тилни танланг 👇🏻\n\nЗдраствуйте уважаемый пользватель 👋\nДобро пожаловать на официальный бот \"BB Logistics\" 🚛\nПожалуйста выберите язык 👇🏻',
                               reply_markup=til())


@dp.callback_query_handler(state='change_lang')
async def change(call: CallbackQuery, state: FSMContext):
    register_user(user=call.from_user.id, lang=call.data, ism=call.from_user.first_name)
    await call.message.delete()
    if call.data == 'uz':
        text = 'Сиз Узбек 🇺🇿 тилини танладингиз'
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=mainkeys(call.data))
    else:
        text = 'Вы выбрали Русский язык 🇷🇺.'
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=mainkeys(call.data))
    await state.set_state('get_com')


@dp.callback_query_handler(state='delete_request')
async def del_request(call: types.CallbackQuery, state: FSMContext):
    id = call.from_user.id
    data = call.data
    delete_request(user_id=id, req_id=data)
    await call.message.delete()
    if gg(id)[0] == 'uz':
        await bot.send_message(chat_id=call.from_user.id, text='👤 Шахсий кабинет', parse_mode='HTML',
                               reply_markup=mainkeys(gg(id)[0]))
        await state.set_state('get_com')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='👤 Личный кабинет', parse_mode='HTML',
                               reply_markup=mainkeys(gg(id)[0]))
        await state.set_state('get_com')
    await state.set_state('get_com')


@dp.callback_query_handler(state='get_info')
async def get_by_id(call: CallbackQuery, state: FSMContext):
    if gg(call.from_user.id):
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='⏳')
        url = 'http://185.65.202.117:7979/leads/'
        numb = call.data
        resp = requests.get(url + numb)
        a = resp.json()
        # print("Qaniii: ", a)
        cont = ''
        data = ''
        mesto = ''
        disl = ''
        punkt = ''
        yon = ''
        otp = ''
        kont = ''
        avto = ''
        avia = ''
        vagon = ''
        prib = ''
        oplata = ''
        ros = ''
        if a.get('id'):
            cost = a.get('price')
            a = a.get('custom_fields_values')

            # print(a)
            text = f'🆔 {numb} ✅\n'
            for i in a:
                if i.get('field_name') == 'Номер контейнера':
                    cont += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Дата погрузки':
                    data += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Место погрузки':
                    mesto += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Дислокация':
                    disl += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Расстояние':
                    ros += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Пункт назначения':
                    punkt += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Дата отправки':
                    otp += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Yo\'nalish':
                    yon += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Контейнер':
                    kont += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Авто':
                    avto += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Авиа':
                    avia += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Вагон':
                    vagon += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Дата прибытие':
                    prib += i.get('values')[0].get('value')
                elif i.get('field_name') == 'Оплата (Дата-Сумма)':
                    oplata += i.get('values')[0].get('value')
            # if oplata:
            #         # print(oplata)
            #     oplata = oplata.split("/")
            #     oplata = oplata[0].split('$')
            # else:
            #     oplata = '0'                
            
            if gg(call.from_user.id)[0] == 'uz':
                # text += f'💵 <b>Бюджет</b>: ${cost}\n'
                # if oplata != '':
                #     text += f'💰 <b>Тўлов (сана-сумма)</b>: {oplata}\n'
                # if oplata == '':
                #     text += f'💰 <b>Тўлов (сана-сумма)</b>: ----- \n'
                if cont:
                    text += f'🔢 <b>Контейнер рақами</b>: {cont}\n'
                if kont != '':
                    text += f'⏺ <b>Контейнер</b>: {kont}\n'
                if avto != '':
                    text += f'🚛 <b>Авто</b>: {avto}\n'
                if avia != '':
                    text += f'✈️ <b>Авиа</b>: {avia}\n'
                if vagon != '':
                    text += f'🚋 <b>Вагон</b>: {vagon}\n'
                if data:
                    text += f'📅 <b>Юклаш санаси</b>: {data}\n'
                if mesto:
                    text += f'🌏 <b>Юклаш манзили</b>: {mesto}\n'
                if otp:
                    text += f'📅 <b>Юбориш санаси</b>: {otp}\n'
                if disl:
                    text += f'📍 <b>Дислокация</b>: {disl}\n'
                if ros:
                    text += f'↔️ <b>Масофа</b>: {ros}\n'
                if punkt:
                    text += f'🏁️ <b>Етказиш манзили</b>: {punkt}\n'
                if prib:
                    text += f'📅 <b>Келиш санаси</b>: {prib}\n'
                if yon:
                    text += f'🌐 <b>Йўналиш манзили</b>: {yon}\n'
                txt = "👤 Шахсий кабинет"
            else:
                txt = '👤 Личный кабинет'
                # text += f'💵 <b>Бюджет</b>: ${cost}\n'
                # if oplata != '':
                #     text += f'💰 <b>Оплата (Дата-Сумма)</b>: {oplata}\n'
                # if oplata == '':
                #     text += f'💰 <b>Оплата (Дата-Сумма)</b>: -- -- \n'
                if cont:
                    text += f'🔢 <b>Номер контейнера</b>: {cont}\n'
                if kont != '':
                    text += f'⏺ <b>Контейнер</b>: {kont}\n'
                if avto != '':
                    text += f'🚛 <b>Авто</b>: {avto}\n'
                if avia != '':
                    text += f'✈️ <b>Авиа</b>: {avia}\n'
                if vagon != '':
                    text += f'🚋 <b>Вагон</b>: {vagon}\n'
                if data:
                    text += f'📅 <b>Дата погрузки</b>: {data}\n'
                if mesto:
                    text += f'🌏 <b>Место погрузки</b>: {mesto}\n'
                if otp:
                    text += f'📅 <b>Дата отправки</b>: {otp}\n'
                if disl:
                    text += f'📍 <b>Дислокация</b>: {disl}\n'
                if ros:
                    text += f'↔️ <b>Расстояние</b>: {ros}'
                if prib:
                    text += f'📅 <b>Дата прибытие</b>: {prib}\n'
                if yon:
                    text += f'🌐 <b>Место направление</b>: {yon}\n'
                if punkt:
                    text += f'🏁️ <b>Место доставки</b>: {punkt}\n'

            await bot.delete_message(message_id=call.message.message_id + 1, chat_id=call.from_user.id, )
            await bot.send_message(text=text, chat_id=call.from_user.id,
                                   parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

            await bot.send_message(text=txt, chat_id=call.from_user.id, parse_mode='HTML',
                                   reply_markup=mainkeys(gg(call.message.chat.id)[0]))
            await state.set_state('get_com')
        else:
            if gg(call.from_user.id)[0] == 'uz':
                await bot.edit_message_text(text='Бундай ID ли контейнер мавжуд эмас ❌',
                                            message_id=call.message.message_id + 1,
                                            chat_id=call.from_user.id, parse_mode='HTML')
            else:
                await bot.edit_message_text(text='Не сущеуствует контейнер с таким ID ❌',
                                            message_id=call.message.message_id + 1,
                                            chat_id=call.from_user.id, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=call.from_user.id,
                               text='Илтимос тилни танланг 👇🏻\n\nПожалуйста выберите язык 👇🏻',
                               reply_markup=til())


@dp.callback_query_handler(state='get_finance')
async def get_by_id(call: CallbackQuery, state: FSMContext):
    if gg(call.from_user.id):
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text='⏳')
        url = 'http://185.65.202.117:7979/leads/'
        numb = call.data
        resp = requests.get(url + numb)
        cost = ''
        oplata = ''
        a = resp.json()
        if a.get('id'):
            cost = a.get('price')
            a = a.get('custom_fields_values')

            text = f'🆔 {numb} ✅\n'
            for i in a:
                if i.get('field_name') == 'Оплата (Дата-Сумма)':
                    oplata += i.get('values')[0].get('value')
            # print("AAAAAAAAAAA", oplata)
            # oplata = '220$ / 09.09.2022 / ✅ '
            # oplata = oplata.replace("/ ??", "")
            # print(oplata)
            # oplata = oplata.split("/ ??")
            # oplata.remove(oplata[len(oplata) - 1])
            if "+" in oplata or '-' in oplata:                
                oplata = oplata.split("//")
                if gg(call.from_user.id)[0] == 'uz':
                    text += f'💵 <b>Бюджет</b>: ${cost}\n\n'
                    if oplata != ['']:
                        print(oplata)
                        opl = 0
                        n = 1
                        for i in oplata:
                            i = i.split("/")
                            print(i)
                            text += f'{n}) <b>Тўлов </b>: {i[0]}\n'
                            text += f'     <b>Сана </b>: {i[1]}'
                            if '+' in i[2]:
                                text += " / <b>Қабул қилинди</b> ✅\n\n"
                            elif '-' in i[2]:
                                text += " / <b>Қабул қилинмади</b> ❌\n\n"
                            else:
                                text += "\n\n"

                            opl += int(i[0].split('$')[0])
                            n += 1
                        text += f"   <b>💰 Қолдиқ</b> : ${int(cost)-opl}"
                            
                    if oplata == ['']:
                        text += f'💰 <b>Тўлов (сана-сумма)</b>: ----- \n'
                    txt = "👤 Шахсий кабинет"
                else:
                    txt = '👤 Личный кабинет'
                    text += f'💵 <b>Бюджет</b>: ${cost}\n'
                    if oplata != ['']:
                        opl = 0
                        n = 1
                        for i in oplata:
                            i = i.split("/")
                            text += f'{n}) <b>Оплата </b>: {i[0]}\n'
                            text += f'     <b>Дата </b>: {i[1]}'
                            if '✅' in i[2]:
                                text += " / <b>Принято</b> ✅\n\n"
                            elif '❌' in i[2]:
                                text += " / <b>Не принято</b> ❌\n\n"
                            else:
                                text += "\n\n"
                            opl += int(i[0].split('$')[0])
                            n += 1
                        text += f"   <b>Осталось</b> : ${int(cost)-opl}"
                    if oplata == ['']:
                        text += f'💰 <b>Оплата (Дата-Сумма)</b>: -- -- \n'
            else:
                oplata = oplata.split("/ ??")
                oplata.remove(oplata[len(oplata) - 1])
                if gg(call.from_user.id)[0] == 'uz':
                    text += f'💵 <b>Бюджет</b>: ${cost}\n\n'
                    if oplata != ['']:
                        opl = 0
                        n = 1
                        for i in oplata:
                            i = i.split("/")
                            print(i)
                            text += f'{n}) <b>Тўлов </b>: {i[0]}\n'
                            text += f'     <b>Сана </b>: {i[1]}'
                            text += "\n\n"

                            opl += int(i[0].split('$')[0])
                            n += 1
                        text += f"   <b>💰 Қолдиқ</b> : ${int(cost)-opl}"
                            
                    if oplata == ['']:
                        text += f'💰 <b>Тўлов (сана-сумма)</b>: ----- \n'
                    txt = "👤 Шахсий кабинет"
                else:
                    txt = '👤 Личный кабинет'
                    text += f'💵 <b>Бюджет</b>: ${cost}\n'
                    if oplata != ['']:
                        opl = 0
                        n = 1
                        for i in oplata:
                            i = i.split("/")
                            text += f'{n}) <b>Оплата </b>: {i[0]}\n'
                            text += f'     <b>Дата </b>: {i[1]}'
                            text += "\n\n"
                            opl += int(i[0].split('$')[0])
                            n += 1
                        text += f"   <b>Осталось</b> : ${int(cost)-opl}"
                    if oplata == ['']:
                        text += f'💰 <b>Оплата (Дата-Сумма)</b>: -- -- \n'
                        
            await bot.delete_message(message_id=call.message.message_id + 1, chat_id=call.from_user.id, )
            await bot.send_message(text=text, chat_id=call.from_user.id,
                                   parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

            await bot.send_message(text=txt, chat_id=call.from_user.id, parse_mode='HTML',
                                   reply_markup=mainkeys(gg(call.message.chat.id)[0]))
            await state.set_state('get_com')
        else:
            if gg(call.from_user.id)[0] == 'uz':
                await bot.edit_message_text(text='Бундай ID ли контейнер мавжуд эмас ❌',
                                            message_id=call.message.message_id + 1,
                                            chat_id=call.from_user.id, parse_mode='HTML')
            else:
                await bot.edit_message_text(text='Не сущеуствует контейнер с таким ID ❌',
                                            message_id=call.message.message_id + 1,
                                            chat_id=call.from_user.id, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=call.from_user.id,
                               text='Илтимос тилни танланг 👇🏻\n\nПожалуйста выберите язык 👇🏻',
                               reply_markup=til())

