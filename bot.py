import requests
import json
from bot_token import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def start_command_message(message: Message):
    await message.answer('Йоу собаки, я Наруто Узумаки!!!')

    


@dp.message(Command(commands=['help']))
async def help_command_message(message: Message):
    await message.answer('Да я толком ничего не умею))')


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип не поддерживается')


if __name__ == '__main__':
    dp.run_polling(bot)

