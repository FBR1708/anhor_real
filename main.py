from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from Token import dp
from database import Session, Base, engine
from uzb_language.menu_uzb import start, check_cart, clear_cart, lotin_menu, increase_quantity, savat, \
    inline_button_food, Form, phone_number, phone_number1, phone, location, send_group_user_info

Base.metadata.create_all(engine)

session = Session()


@dp.message_handler(commands=['start'])
async def handle_message(message: types.Message):
    await start(message)


@dp.message_handler(lambda message: message.text == '🇺🇿 Uzbek')
async def handle_message(message: types.Message):
    await lotin_menu(message)


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
                                                  'Tasdiqlash', 'O\'zgartirish', 'To\'lovni amalga oshirish'])
async def handle_message(message: types.Message):
    await inline_button_food(message)


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


# @dp.message_handler(lambda message: message.text == 'Click')
# async def handle_message(message: types.Message):
#     await phone(message)

#
# @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
# async def handle(message: types.Message):
#     await sddd(message)


@dp.callback_query_handler(lambda query: True and query.data != 'savat')
async def handle_inline_btn_and_food_sum(callback_query: types.CallbackQuery):
    await increase_quantity(callback_query)


@dp.callback_query_handler(lambda query: query.data == 'savat')
async def handle_message(callback_query: types.CallbackQuery):
    await savat(callback_query)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text='Bizda bunday buyruq mavjud emas.   /    У нас нет такoгo приказа.',
                         reply=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
