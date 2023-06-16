from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

reg = KeyboardButton("Регистрация")
gender1 = KeyboardButton("Мужчина")
gender2 = KeyboardButton("Женщина")

kb_gender = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_gender.add(gender1,gender2)

kb_reg = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_reg.add(reg)