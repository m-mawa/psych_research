from aiogram import types, Dispatcher
from dispatcher import dp
import aioschedule
import asyncio
import logging
from aiogram.types.input_file import InputFile
from db import BotDB

async def export_table(message: types.Message):
    try:
        BotDB.records_to_csv()
        doc1 = InputFile('./records.csv')
        await message.bot.send_document(message.from_user.id, doc1)
        BotDB.users_to_csv()
        doc2 = InputFile('./users.csv')
        await message.bot.send_document(message.from_user.id, doc2)
    except Exception as e:
        logging.exception(e)
        await message.reply('Произошла ошибка при выполнении команды')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(export_table, commands=["Выгрузить данные в таблицу"])
    dp.register_message_handler(export_table, text=["Выгрузить данные в таблицу"])
