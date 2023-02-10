from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5151526365:AAEvgNp7MLewmjsgRzVLlTwmITday-qymEQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
admins = [935567645]
