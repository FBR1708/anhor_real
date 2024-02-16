from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from Token import bot
from database import Session, MainMenu, Menu
from rus_language.menu_rus import kril_menu
from uzb_language.keyboard_uzb import language, pay, pay1, contact1, user_location, keyboard7, keyboard8
import re


# Payment_Token = '371317599:TEST:1707458286298'
# Click_Token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'


class Form(StatesGroup):
    phone_number = State()
    location = State()


quantity = 1
total_amount = 0
current_product = None


async def start(message: types.Message):
    await message.answer("Тилни танланг  /   Выберите язык", reply_markup=language)


async def lotin_menu(message: types.Message):
    db = Session()
    food_items = db.query(MainMenu).all()
    db.close()
    global keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text='⬅Ortga'))
    keyboard.add(KeyboardButton(text='Savat🧺'))
    buttons = [KeyboardButton(text=food_item.name) for food_item in food_items]
    for i in range(0, len(buttons), 2):
        row = buttons[i:i + 2]
        keyboard.add(*row)

    await message.answer("Nima buyurtma qilasiz?", reply_markup=keyboard)


async def on_inline_button_click(callback_query: types.CallbackQuery):
    if callback_query.data == 'ortga':
        await lotin_menu(callback_query.message)


async def update_inline_keyboard(callback_query):
    global quantity, total_amount, current_product

    ikm = InlineKeyboardMarkup()
    ikm.add(
        InlineKeyboardButton("+", callback_data='increase_quantity'),
        InlineKeyboardButton(str(quantity), callback_data='quantity'),
        InlineKeyboardButton("-", callback_data='decrease_quantity'),
        InlineKeyboardButton(f"{total_amount} sum", callback_data='summa'),
        InlineKeyboardButton("Savatga 📩", callback_data='savat')
    )

    if callback_query.message.reply_markup != ikm:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=ikm
        )


async def increase_quantity(callback_query: types.CallbackQuery):
    global quantity, total_amount, current_product
    try:
        data = callback_query.data
        global db
        db = Session()
        if data == 'increase_quantity':
            quantity += 1
        elif data == 'decrease_quantity' and quantity > 1:
            quantity -= 1
        else:
            food_item = db.query(Menu).filter(Menu.callback_data == data).first()
            if food_item:
                current_product = food_item
                quantity = 1
        total_amount = int(quantity) * int(current_product.price) if current_product else current_product.price
        await update_inline_keyboard(callback_query)

    finally:
        db.close()


user_carts = {}


async def check_cart(chat_id):
    if chat_id not in user_carts or not user_carts[chat_id]:
        await bot.send_message(chat_id, "Savat bo'sh. Sizda buyurtma mavjud emas.")
        return

    global total_cart_amount
    total_cart_amount = 0
    message = "Savatchadagi mahsulotlar:\n\n"

    global product_name, quantity, price, amount, index
    for index, item in enumerate(user_carts[chat_id], start=1):
        product_name = item['product_name']
        quantity = item['quantity']
        price = item['price']
        amount = item['amount']

        message += f"{index}. {product_name}\nMiqdor: {quantity} dona \nNarxi: {price} sum \nJami: {amount} sum\n\n"
        total_cart_amount += amount

    message += f"\nJami savatcha summasi: {total_cart_amount} sum"
    await bot.send_message(chat_id, message, reply_markup=pay)


async def savat(callback_query: types.CallbackQuery):
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

            await update_inline_keyboard(callback_query)
            await bot.send_message(chat_id, text="Mahsulot qoshildi", reply_markup=keyboard)
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
    finally:
        db.close()


async def inline_button_food(message: types.Message):
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

                    reply_markup.add(InlineKeyboardButton(text='🔙Ortga', callback_data='ortga'))
                    await bot.send_photo(message.chat.id, photo=menu.food_picture, reply_markup=reply_markup)
                else:
                    await message.answer("No food items found for the selected MainMenu.")
        else:
            await message.answer("MainMenu not found.")

    finally:
        db.close()


async def phone(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        await message.answer("Telefon raqamini faqat shaxsiy chatlarda so'rash mumkin.")
        return
    # global xz_turi
    # xz_turi = message.text
    # async with state.proxy() as data:
    #     data['pay_type'] = message.text
    await message.answer(
        "Telefon raqamingizni pastdagi tugma orqali kiriting. Yoki shablon orqali  kiriting:\n M-n:  +998 XX XXX XX XX",
        reply_markup=contact1)
    await Form.phone_number.set()


async def phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
    await Form.next()
    await message.answer('Manzilni jo\'nating', reply_markup=user_location)


async def phone_number1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        phone_number = message.text
        if validate_phone_number(phone_number):
            data['phone_number'] = phone_number
        else:
            await message.answer("Noto'g'ri formatdagi telefon raqamini kiritdingiz. Iltimos, qaytadan kiriting.")
            return
    await Form.next()
    await message.answer('Manzilni jo\'nating', reply_markup=user_location)


def validate_phone_number(phone_number):
    phone_regex_with_spaces = re.compile(r'^\+998 \d{2} \d{3} \d{2} \d{2}$')
    phone_regex_without_spaces = re.compile(r'^\+998\d{9}$')
    if phone_regex_with_spaces.match(phone_number) or phone_regex_without_spaces.match(phone_number):
        return True
    else:
        return False


# async def product(message: types.Message):
#     if Payment_Token.split(':')[1] == 'TEST':
#         PRICE = types.LabeledPrice(label="Umumiy summa", amount=total_cart_amount * 100)
#         await bot.send_invoice(
#             chat_id=message.chat.id,
#             title='Buyurtmangizdan mamnunmiz!',
#             description="Payment to\'lov tizimi",
#             provider_token=Payment_Token,
#             currency="UZS",
#             prices=[PRICE],
#             start_parameter="one-month-subscription",
#             payload="test-invoice-payload"
#         )


# async def sddd(message: types.Message):
#     payment_info = message.successful_payment.to_python()
#     for k, x in payment_info.items():
#         print(k, x)
#         await bot.send_message(message.chat.id, f"Shunchaki foidanaluvchi uchun tolandi qismi...")
#         # await bot.send_message(config.ADMINS[0], f"To'langandan so'ng adminga habar yuborish uchun...")


async def location(message: types.Message, state: FSMContext):
    global loc, user_id, loc1, v, user_phone
    loc = message.location
    user_id = message.chat.id
    loc1 = message.message_id
    async with state.proxy() as data:
        data['location'] = message.location
    user_phone = data['phone_number']
    v = f"🛑 To\'lov  turi: Naqd\n 🛑 Telefon raqam  :   {data['phone_number']}\n 🛑 Yetkazib berish xizmati pullik. \n\n🛑 Ma'lumotlar to'g'riligini tekshiring va pastdagi tugma orqali tasdiqlang."
    await bot.send_message(user_id, v, reply_markup=keyboard7)
    await state.finish()

    # elif xz_turi == 'Click':
    #     async with state.proxy() as data:
    #         data['location'] = message.location
    #     user_id = message.chat.id
    #     pay_type = data['pay_type']
    #     v1 = f"🛑 To\'lov  turi: {pay_type}\n 🛑 Telefon raqam  :   {data['phone_number']}\n\n🛑 Ma'lumotlar to'g'riligini tekshiring va pastdagi tugma orqali tasdiqlang."
    #     await bot.send_message(user_id, v1, reply_markup=keyboard8)
    #     await state.finish()


async def clear_cart(message: types.Message, chat_id: int):
    if chat_id in user_carts:
        del user_carts[chat_id]
    await message.answer("Savat tozalandi.", reply_markup=pay)


async def send_group_user_info(message: types.Message, state: FSMContext):
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
    await message.answer('Ma\'lumotlar adminga yuborildi tez orada siz bilan aloqaga chiqishadi',
                         reply_markup=language)
    chat_id = message.chat.id
    if chat_id in user_carts:
        del user_carts[chat_id]
    await state.finish()

# async def pay1_button(message: types.Message):
#     await message.answer(text='To\'lovni qaysi turda amalga oshirmoqchisiz?', reply_markup=pay1)
