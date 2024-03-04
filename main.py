from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from Token import dp
from database import Session
from rus_language.menu_rus import kril_menu, check_cart_ru, inline_button_food_ru, phone_ru, clear_cart_ru, \
    send_group_user_info_ru, phone_number_ru, phone_number1_ru, location_ru, increase_quantity_ru, savat_ru, Form_ru, \
    on_inline_button_click_ru
from uzb_language.menu_uzb import start, check_cart, clear_cart, lotin_menu, increase_quantity, savat, \
    inline_button_food, Form, phone_number, phone_number1, phone, location, send_group_user_info, on_inline_button_click

session = Session()


@dp.message_handler(commands=['start'])
async def handle_message(message: types.Message):
    await start(message)


@dp.message_handler(lambda message: message.text == '🇺🇿 Uzbek')
async def handle_message(message: types.Message):
    global lang
    lang = '🇺🇿 Uzbek'
    await lotin_menu(message)


@dp.message_handler(lambda message: message.text == '🇷🇺 Russia')
async def handle_message(message: types.Message):
    global lang
    lang = '🇷🇺 Russia'
    await kril_menu(message)


@dp.callback_query_handler(
    lambda query: True and query.data != 'savat' and query.data != 'savat_ru' and query.data != 'ortga' and query.data != 'ortga_ru')
async def handle_inline_btn_and_food_sum(callback_query: types.CallbackQuery):
    if lang == '🇺🇿 Uzbek':
        await increase_quantity(callback_query)
    elif lang == '🇷🇺 Russia':
        await  increase_quantity_ru(callback_query)


@dp.message_handler(lambda message: message.text == 'Savat🧺')
async def handle_message(message: types.Message):
    await check_cart(message.chat.id)


@dp.message_handler(lambda message: message.text == '🔙Ortga' or message.text == '⬅Ortga' or message.text == '🔚Ortga')
async def handle_message(message: types.Message):
    if message.text == '🔙Ortga':
        await lotin_menu(message)
    elif message.text == '⬅Ortga':
        await start(message)
    elif message.text == '🔚Ortga':
        await check_cart(message.chat.id)


@dp.message_handler(
    lambda message: True and message.text not in ['Savat🧺', 'Buyurtmani rasmiylashtirish', '🔙Ortga', '⬅Ortga',
                                                  'Savatni tozalash', 'Click', 'Naqd', '🔚Ortga', 'Manzilni yuborish',
                                                  'Tasdiqlash', 'O\'zgartirish', 'To\'lovni amalga oshirish',
                                                  'Корзина🧺', '🔙Назад', '⬅Назад', '🔚Назад', 'Обработка заказа',
                                                  'Очистить корзину', 'Подтверждение', 'Изменять', '🇷🇺 Russia',
                                                  '🇺🇿 Uzbek'])
async def handle_message(message: types.Message):
    if lang == '🇺🇿 Uzbek':
        await inline_button_food(message)
    elif lang == '🇷🇺 Russia':
        await inline_button_food_ru(message)


@dp.message_handler(lambda message: message.text == 'Buyurtmani rasmiylashtirish')
async def handle_message(message: types.Message):
    await phone(message)


@dp.message_handler(lambda message: message.text == 'Savatni tozalash')
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    await clear_cart(message, chat_id)


#
# @dp.message_handler(lambda message: message.text in ['Naqd'])
# async def handle_message(message: types.Message):
#     await phone(message)


@dp.message_handler(content_types=types.ContentType.CONTACT,
                    state=Form.phone_number)
async def handle_message(message: types.Message, state: FSMContext):
    await phone_number(message, state)


@dp.message_handler(state=Form.phone_number)
async def handle_message(message: types.Message, state: FSMContext):
    await phone_number1(message, state)


@dp.message_handler(state=Form.location, content_types=types.ContentType.LOCATION)
async def handle_message(message: types.Message, state: FSMContext):
    await location(message, state)


@dp.message_handler(lambda message: message.text in ['Tasdiqlash'])
async def handle_message(message: types.Message, state: FSMContext):
    await send_group_user_info(message, state)


# @dp.message_handler(lambda message: message.text in ['To\'lovni amalga oshirish'])
# async def handle_message(message: types.Message):
#     await product(message)


@dp.message_handler(lambda message: message.text in ['O\'zgartirish'])
async def handle_message(message: types.Message):
    await phone(message)


@dp.callback_query_handler(lambda query: query.data == 'savat')
async def handle_message(callback_query: types.CallbackQuery):
    await savat(callback_query)


@dp.callback_query_handler(lambda query: query.data == 'savat_ru')
async def handle_message(callback_query: types.CallbackQuery):
    await savat_ru(callback_query)


@dp.callback_query_handler(lambda query: query.data in ['ortga', 'ortga_ru'])
async def handle_message(callback_query: types.CallbackQuery):
    if callback_query.data == 'ortga':
        await on_inline_button_click(callback_query)
    elif callback_query.data == 'ortga_ru':
        await on_inline_button_click_ru(callback_query)


# '================================================================================================================='


@dp.message_handler(lambda message: message.text == 'Корзина🧺')
async def handle_message(message: types.Message):
    await check_cart_ru(message.chat.id)


@dp.message_handler(lambda message: message.text == '🔙Назад' or message.text == '⬅Назад' or message.text == '🔚Назад')
async def handle_message(message: types.Message):
    if message.text == '🔙Назад':
        await kril_menu(message)
    elif message.text == '⬅Назад':
        await start(message)
    elif message.text == '🔚Назад':
        await check_cart_ru(message.chat.id)


# @dp.message_handler(
#     lambda message: True and message.text not in ['Savat🧺', 'Buyurtmani rasmiylashtirish', '🔙Ortga', '⬅Ortga',
#                                                   'Savatni tozalash', 'Click', 'Naqd', '🔚Ortga', 'Manzilni yuborish',
#                                                   'Tasdiqlash', 'O\'zgartirish', 'To\'lovni amalga oshirish',
#                                                   'Корзина🧺', '🔙Назад', '⬅Назад', '🔚Назад', 'Обработка заказа',
#                                                   'Очистить корзину', 'Подтверждение', 'Изменять', '🇷🇺 Russia'])
# async def handle_message(message: types.Message):
#     await inline_button_food_ru(message)


@dp.message_handler(lambda message: message.text == 'Обработка заказа')
async def handle_message(message: types.Message):
    await phone_ru(message)


@dp.message_handler(lambda message: message.text == 'Очистить корзину')
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    await clear_cart_ru(message, chat_id)


@dp.message_handler(content_types=types.ContentType.CONTACT,
                    state=Form_ru.phone_number_ru)
async def handle_message(message: types.Message, state: FSMContext):
    await phone_number_ru(message, state)


@dp.message_handler(state=Form_ru.phone_number_ru)
async def handle_message(message: types.Message, state: FSMContext):
    await phone_number1_ru(message, state)


@dp.message_handler(state=Form_ru.location_ru, content_types=types.ContentType.LOCATION)
async def handle_message(message: types.Message, state: FSMContext):
    await location_ru(message, state)


@dp.message_handler(lambda message: message.text in ['Подтверждение'])
async def handle_message(message: types.Message, state: FSMContext):
    await send_group_user_info_ru(message, state)


@dp.message_handler(lambda message: message.text in ['Изменять'])
async def handle_message(message: types.Message):
    await phone_ru(message)


# @dp.message_handler(lambda message: message.text == 'Click')
# async def handle_message(message: types.Message):
#     await phone(message)

#
# @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
# async def handle(message: types.Message):
#     await sddd(message)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text='Bizda bunday buyruq mavjud emas.   /    У нас нет такoгo приказа.',
                         reply=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

d = 20