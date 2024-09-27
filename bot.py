from bot_token import TOKEN
from aiogram import Bot, Dispatcher
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
    await message.reply(text=f'Вот что ты мне прислал - {message.text}')

if __name__ == '__main__':
    dp.run_polling(bot)

