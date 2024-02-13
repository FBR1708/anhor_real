from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_button = [
    [KeyboardButton(text='🇺🇿 Uzbek'),
     KeyboardButton(text='🇷🇺 Russia'),
     ],
]

language = ReplyKeyboardMarkup(keyboard=keyboard_button, resize_keyboard=True, row_width=1)

keyboard_button1 = [
    [KeyboardButton(text='⬅Ortga'),
     KeyboardButton(text='Savat🧺'),
     ],
]
menu_main = ReplyKeyboardMarkup(keyboard=keyboard_button1, resize_keyboard=True, row_width=1)

keyboard_button2 = [
    [KeyboardButton(text='Buyurtmani rasmiylashtirish'),
     KeyboardButton(text='Savatni tozalash')], [KeyboardButton(text='🔙Ortga'), ]
]
pay = ReplyKeyboardMarkup(keyboard=keyboard_button2, resize_keyboard=True, row_width=1)

keyboard_button3 = [
    [KeyboardButton(text='Click'),
     KeyboardButton(text='Naqd')], [KeyboardButton(text='🔚Ortga')]
]
pay1 = ReplyKeyboardMarkup(keyboard=keyboard_button3, resize_keyboard=True, row_width=1)

contact1 = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [KeyboardButton(text='Tugma orqali', request_contact=True),
                                    ]], row_width=1
                               )

user_location = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [KeyboardButton(text='Manzilni yuborish', request_location=True),
                                         ]], row_width=1
                                    )

keyboard7 = ReplyKeyboardMarkup(resize_keyboard=True,
                                keyboard=[
                                    [KeyboardButton(text='Tasdiqlash'),
                                     KeyboardButton(text='O\'zgartirish'),
                                     ]], row_width=1
                                )

keyboard8 = ReplyKeyboardMarkup(resize_keyboard=True,
                                keyboard=[
                                    [KeyboardButton(text='To\'lovni amalga oshirish'),
                                     KeyboardButton(text='O\'zgartirish'),
                                     ]], row_width=1
                                )
