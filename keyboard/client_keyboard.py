from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton("Добавить запись")
b2 = KeyboardButton("Выгрузить данные в таблицу")
b3 = KeyboardButton("Тест ПЭ состояния")
mood1 = KeyboardButton("Все хорошо 🙂")
mood2 = KeyboardButton("Что-то расстроило 😣")
mood3 = KeyboardButton("Нейтральное 😐")
mood4 = KeyboardButton("Злюсь 😡")
inT = KeyboardButton("Да")
inF = KeyboardButton("Нет")
cancle_but = KeyboardButton("Отмена")
urlTest = InlineKeyboardButton(text="Тест Люшера", url = 'https://psytests.org/luscher/8color-run.html')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3)

kb_mood = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_mood.add(mood1).add(mood2).add(mood3).add(mood4).add(cancle_but)

kb_injuries = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_injuries.row(inT, inF)

kb_url = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_url.add(urlTest)