from aiogram import types, Dispatcher
from dispatcher import dp
import config
import re
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard import kb_client, kb_mood, kb_injuries, kb_url
from db import BotDB
import aioschedule
import asyncio
import logging

class FSMUser(StatesGroup):
    test = State()
    mood_m = State()
    mood_w = State()
    mood_n = State()
    injuries = State()

""" async def on_startup(_):
    aioschedule.every().day.at("21:38").do(start) """

async def test(message: types.Message):
    await message.reply("Ссылочка: ", reply_markup=kb_url)

#@dp.message_handler(commands="Добавить запись", state=None)
async def rc_start(message: types.Message):
    await FSMUser.test.set()
    await message.reply("Пройдите тест ПЭ состояния: ", reply_markup=kb_url)
    await message.reply("Введите полученный показатель тревожности: ")
    
async def load_test(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["test"] = message.text  
    await FSMUser.next()
    await message.reply("Настроение утром", reply_markup=kb_mood)

#@dp.message_handler(state=FSMUser.mood_m)
async def load_mmood(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["mood_m"] = message.text
    await FSMUser.next()
    await message.reply("Настроение в течение рабочего дня", reply_markup=kb_mood)

#@dp.message_handler(state=FSMUser.mood_w)
async def load_wmood(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["mood_w"] = message.text
    await FSMUser.next()
    await message.reply("Настроение в конце рабочего дня (сейчас)", reply_markup=kb_mood)

#@dp.message_handler(state=FSMUser.mood_n)
async def load_nmood(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["mood_n"] = message.text
    await FSMUser.next()
    await message.reply("Было ли обращение в мед.часть с микротравмой?", reply_markup=kb_injuries)

#@dp.message_handler(state=FSMUser.injuries)
async def load_injuries(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["injuries"] = message.text
    await message.reply("Спасибо! До завтра.", reply_markup=kb_client)
    await BotDB.add_record(state)
    await state.finish()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    try:
        await state.finish()
        await message.reply("Сработала отмена", reply_markup=kb_client)
    except Exception as e:
        logging.exception(e)
        await message.reply('Произошла ошибка при выполнении команды')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(test, text=["Тест ПЭ состояния"])
    dp.register_message_handler(rc_start, text=["Добавить запись"], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=["Отмена"])
    dp.register_message_handler(cancel_handler, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(load_test, state=FSMUser.test)
    dp.register_message_handler(load_mmood, state=FSMUser.mood_m)
    dp.register_message_handler(load_wmood, state=FSMUser.mood_w)
    dp.register_message_handler(load_nmood, state=FSMUser.mood_n)
    dp.register_message_handler(load_injuries, state=FSMUser.injuries)
    
    
