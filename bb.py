from aiogram import executor
import logging
from bot_token import dp
import msg_handler


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
