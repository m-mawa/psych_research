from aiogram import executor
from dispatcher import dp

from handlers import personal_actions, admin_actions, registration



personal_actions.register_handlers_user(dp)

""" from db import BotDB
BotDB = BotDB('accountant.db') """

registration.register_handlers_reg(dp)
personal_actions.register_handlers_user(dp)
admin_actions.register_handlers_admin(dp)

""" , on_startup=personal_actions.on_startup """

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
