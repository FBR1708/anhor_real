from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_button1 = [
    [KeyboardButton(text='⬅Назад'),
     KeyboardButton(text='Корзина🧺'),
     ],
]
menu_main_ru = ReplyKeyboardMarkup(keyboard=keyboard_button1, resize_keyboard=True, row_width=1)

keyboard_button2 = [
    [KeyboardButton(text='Обработка заказа'),
     KeyboardButton(text='Очистить корзину')], [KeyboardButton(text='🔙Назад'),]
]
pay_ru = ReplyKeyboardMarkup(keyboard=keyboard_button2, resize_keyboard=True, row_width=1)



# keyboard_button3 = [
#     [KeyboardButton(text='Click'),
#      KeyboardButton(text='Naqd')], [KeyboardButton(text='🔚Ortga')]
# ]
# pay1 = ReplyKeyboardMarkup(keyboard=keyboard_button3, resize_keyboard=True, row_width=1)

contact1_ru = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [KeyboardButton(text='По кнопке', request_contact=True),
                                    ]], row_width=1
                               )

user_location_ru = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [KeyboardButton(text='Отправить адрес', request_location=True),
                                         ]], row_width=1
                                    )

keyboard7_ru = ReplyKeyboardMarkup(resize_keyboard=True,
                                keyboard=[
                                    [KeyboardButton(text='Подтверждение'),
                                     KeyboardButton(text='Изменять'),
                                     ]], row_width=1
                                )

# keyboard8 = ReplyKeyboardMarkup(resize_keyboard=True,
#                                 keyboard=[
#                                     [KeyboardButton(text='To\'lovni amalga oshirish'),
#                                      KeyboardButton(text='O\'zgartirish'),
#                                      ]], row_width=1
#                                 )
