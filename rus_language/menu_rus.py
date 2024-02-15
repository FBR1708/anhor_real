import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from Token import bot
from database import Session, MainMenu, Menu
from rus_language.keyboard_rus import pay_ru, contact1_ru, user_location_ru, keyboard7_ru
from uzb_language.keyboard_uzb import language


class Form_ru(StatesGroup):
    phone_number_ru = State()
    location_ru = State()


quantity = 1
total_amount = 0
current_product = None


async def kril_menu(message: types.Message):
    global keyboard1
    db = Session()
    food_items = db.query(MainMenu).all()
    db.close()
    keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard1.add(KeyboardButton(text='⬅Назад'))
    keyboard1.add(KeyboardButton(text='Корзина🧺'))
    buttons = [KeyboardButton(text=food_item.name) for food_item in food_items]
    for i in range(0, len(buttons), 2):
        row = buttons[i:i + 2]
        keyboard1.add(*row)

    await message.answer("Что вы заказываете?", reply_markup=keyboard1)


async def update_inline_keyboard_ru(callback_query: types.CallbackQuery):
    global quantity, total_amount, current_product

    ikm1 = InlineKeyboardMarkup()
    ikm1.add(
        InlineKeyboardButton("+", callback_data='increase_quantity_ru'),
        InlineKeyboardButton(str(quantity), callback_data='quantity_ru'),
        InlineKeyboardButton("-", callback_data='decrease_quantity_ru'),
        InlineKeyboardButton(f"{total_amount} sum", callback_data='summa_ru'),
        InlineKeyboardButton("В корзину 📩", callback_data='savat_ru')
    )

    if callback_query.message.reply_markup != ikm1:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=ikm1
        )


async def increase_quantity_ru(callback_query: types.CallbackQuery):
    global quantity, total_amount, current_product
    try:
        data = callback_query.data
        global db
        db = Session()
        if data == 'increase_quantity_ru':
            quantity += 1
        elif data == 'decrease_quantity_ru' and quantity > 1:
            quantity -= 1
        else:
            food_item = db.query(Menu).filter(Menu.callback_data == data).first()
            if food_item:
                current_product = food_item
                quantity = 1
        total_amount = int(quantity) * int(current_product.price) if current_product else current_product.price
        await update_inline_keyboard_ru(callback_query)

    finally:
        db.close()


user_carts = {}


async def check_cart_ru(chat_id):
    if chat_id not in user_carts or not user_carts[chat_id]:
        await bot.send_message(chat_id, "Корзина пуста. У вас нет заказа.")
        return

    global total_cart_amount
    total_cart_amount = 0
    message = "Товары в корзине:\n\n"

    global product_name, quantity, price, amount, index
    for index, item in enumerate(user_carts[chat_id], start=1):
        product_name = item['product_name']
        quantity = item['quantity']
        price = item['price']
        amount = item['amount']

        message += f"{index}. {product_name}\nКоличество: {quantity} dona \nЦена: {price} sum \nОбщая сумма: {amount}  сум\n\n"
        total_cart_amount += amount

    message += f"\nОбщая сумма корзины: {total_cart_amount} сум"
    await bot.send_message(chat_id, message, reply_markup=pay_ru)


async def savat_ru(callback_query: types.CallbackQuery):
    try:
        chat_id = callback_query.message.chat.id

        if chat_id not in user_carts:
            user_carts[chat_id] = []

        global current_product, quantity, total_amount
        if current_product:
            cart_item = {
                'product_name': current_product.name,
                'quantity': quantity,
                'price': current_product.price,
                'amount': total_amount
            }

            user_carts[chat_id].append(cart_item)

            current_product = None
            quantity = 1
            total_amount = 0

            await update_inline_keyboard_ru(callback_query)
            await bot.send_message(chat_id, text="Товар добавлен.", reply_markup=keyboard1)
            message_id_to_delete = callback_query.message.message_id
            await bot.delete_message(chat_id=chat_id, message_id=message_id_to_delete)
    finally:
        db.close()


async def inline_button_food_ru(message: types.Message):
    main_menu_name = message.text
    db = Session()
    try:
        main_menu = db.query(MainMenu).filter(MainMenu.name == main_menu_name).all()
        if main_menu:
            for menu in main_menu:
                food_items = db.query(Menu).filter(Menu.food_id == menu.id).all()
                if food_items:
                    reply_markup = InlineKeyboardMarkup()
                    for food_item in food_items:
                        button_text = f"{food_item.name}"
                        callback_data = food_item.callback_data
                        reply_markup.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

                    await bot.send_photo(message.chat.id, photo=menu.food_picture, reply_markup=reply_markup)
                else:
                    await message.answer("No food items found for the selected MainMenu.")
        else:
            await message.answer("MainMenu not found.")

    finally:
        db.close()


async def phone_ru(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        await message.answer("Номер телефона можно запросить только в приватных чатах.")
        return
    await message.answer(
        "Введите свой номер телефона, используя кнопку ниже. Или введите через шаблон:\n Например:  +998 XX XXX XX XX",
        reply_markup=contact1_ru)
    await Form_ru.phone_number_ru.set()


async def phone_number_ru(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number_ru'] = message.contact.phone_number
    await Form_ru.next()
    await message.answer('Отправить адрес', reply_markup=user_location_ru)


async def phone_number1_ru(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        phone_number = message.text
        if validate_phone_number(phone_number):
            data['phone_number_ru'] = phone_number
        else:
            await message.answer("Вы ввели номер телефона в неправильном формате. Пожалуйста, войдите еще раз.")
            return
    await Form_ru.next()
    await message.answer('Отправить адрес', reply_markup=user_location_ru)


def validate_phone_number(phone_number):
    phone_regex_with_spaces = re.compile(r'^\+998 \d{2} \d{3} \d{2} \d{2}$')
    phone_regex_without_spaces = re.compile(r'^\+998\d{9}$')
    if phone_regex_with_spaces.match(phone_number) or phone_regex_without_spaces.match(phone_number):
        return True
    else:
        return False


async def location_ru(message: types.Message, state: FSMContext):
    global loc, user_id, loc1, v, user_phone
    loc = message.location
    user_id = message.chat.id
    loc1 = message.message_id
    async with state.proxy() as data:
        data['location_ru'] = message.location
    user_phone = data['phone_number_ru']
    v = f"🛑 Тип оплаты: Наличные\n 🛑 Номер телефона  :   {data['phone_number_ru']}\n\n🛑 Проверьте правильность информации и подтвердите ее кнопкой ниже."
    await bot.send_message(user_id, v, reply_markup=keyboard7_ru)
    await state.finish()


async def clear_cart_ru(message: types.Message, chat_id: int):
    if chat_id in user_carts:
        del user_carts[chat_id]
    await message.answer("Корзина очищена.", reply_markup=pay_ru)


async def send_group_user_info_ru(message: types.Message, state: FSMContext):
    user_informations = "Mijoz buyurtmalari:\n\n"
    chat_id = message.chat.id
    for index, item in enumerate(user_carts[chat_id], start=1):
        product_name = item['product_name']
        quantity = item['quantity']
        price = item['price']
        amount = item['amount']
        user_informations += f"{index}. {product_name}\nMiqdor: {quantity} dona \nNarxi: {price} sum \nJami: {amount} sum\n\n"
    user_informations += f"\n🛑 Jami summasi: {total_cart_amount} sum\n"
    user_detail = f"🛑 To\'lov  turi: Naqd\n🛑 Telefon raqam: {user_phone}"
    user_informations += user_detail
    guruh_chat_id = -1002008691273
    await bot.send_location(guruh_chat_id, loc.latitude, loc.longitude)
    await bot.send_message(chat_id=guruh_chat_id, text=user_informations)
    await message.answer('Информация отправлена администратору, они свяжутся с вами в ближайшее время',
                         reply_markup=language)
    chat_id = message.chat.id
    if chat_id in user_carts:
        del user_carts[chat_id]
    await state.finish()
