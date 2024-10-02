from bot_token import TOKEN
import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

bot = Bot(token=TOKEN)
dp = Dispatcher()
ATTEMPTS = 5

user = {'in_game': False,
        'secret_num': None,
        'attempts': None,
        'total_played': 0,
        'wins': 0}


@dp.message(Command(commands='start'))
async def process_start(message: Message):
    await message.answer(f'Првиет {message.chat.first_name}\n'
                         f'Я умею играть в Угадай Число !!\n'
                         'что бы получить больше информации\n'
                         'отправь команду - /help')

if __name__ == '__main__':
    dp.run_polling(bot)