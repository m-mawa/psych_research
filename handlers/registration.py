from aiogram import types, Dispatcher
from dispatcher import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard import kb_gender, kb_reg, kb_client
from db import BotDB
import logging

class NewUser(StatesGroup):
    id = State()
    gender = State()
    age = State()
    education = State()
    shift = State()

async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        try:
            await message.bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=kb_reg)
        except Exception as e:
            logging.exception(e)
            await message.reply('Произошла ошибка при выполнении команды')
    #await message.bot.send_message(message.from_user.id, "Добро пожаловать!")

async def new_user(message: types.Message):
    try:
        await NewUser.id.set()
        await message.reply("Как Вас зовут?")
    except Exception as e:
            logging.exception(e)


async def user_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.from_user.id 
    await message.bot.send_message(message.from_user.id, "Укажите Ваш пол", reply_markup=kb_gender)
    await NewUser.next()

async def user_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["gender"] = message.text
    await NewUser.next()
    await message.reply("Укажите Ваш возраст")

async def user_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text
    await NewUser.next()
    await message.reply("Укажите Ваше образование")

async def user_education(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["education"] = message.text
    await NewUser.next()
    await message.reply("Укажите смену")

async def user_shift(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["shift"] = message.text
    await BotDB.add_user(state)
    await state.finish()
    await message.reply("Регистрация прошла успешно.", reply_markup=kb_client)


def register_handlers_reg(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "help"])
    dp.register_message_handler(new_user,  text=["Регистрация"], state=None)
    dp.register_message_handler(user_id, state=NewUser.id)
    dp.register_message_handler(user_gender, state=NewUser.gender)
    dp.register_message_handler(user_age, state=NewUser.age)
    dp.register_message_handler(user_education, state=NewUser.education)
    dp.register_message_handler(user_shift, state=NewUser.shift)