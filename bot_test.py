from bot_token import TOKEN
import random
import requests
from dataclasses import dataclass

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

bot = Bot(token=TOKEN)
dp = Dispatcher()
ATTEMPTS = 5

animals = {'киска': "('https://api.thecatapi.com/v1/images/search').json()[0]['url']",
           'собачка': "('https://random.dog/woof.json').json()['url']",
           'лисичка': "('https://randomfox.ca/floof/').json()['link']"}

users = {}

@dataclass
class User:
    in_game: bool
    secret_num: int
    attempts: int
    total_played: int
    wins: int


@dp.message(Command(commands='start'))
async def process_start(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = User(False, 0, 0, 0, 0)

    await message.answer(f'Привет {message.chat.first_name}\n'
                         f'Я умею играть в Угадай Число !!\n'
                         'что бы получить больше информации\n'
                         'отправь команду - /help')


@dp.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадаю число от 1 до 100\n'
        f'А тебе надо его угадать\nУ тебя есть {ATTEMPTS} попыток\n'
        f'Доступные команды:\n\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\nЧтобы начать напиши - давай играть)\n\n'
        f'Так же я могу присылать картинки разных животных\n'
        f'Это - киска, собачка и лисичка\n'
        f'Просто напиши, чьё фото ты хочешь'
    )


@dp.message(Command(commands='stat'))
async def process_stat(message: Message):
    await message.answer(
        f'Ты сыграл {users[message.from_user.id].total_played} раз\n'
        f'Из низ ты победил - {users[message.from_user.id].wins}'
    )


@dp.message(Command(commands='cancel'))
async def process_cancel(message: Message):
    if users[message.from_user.id].in_game:
        users[message.from_user.id].in_game = False
        await message.answer('Как хочешь!\nДай знать если захочешь сыграть')
    else:
        await message.answer('А мы ещё не начинали играть)')


@dp.message(F.text.lower().in_(['давай играть', 'давай сыграем', 'играть', 'давай']))
async def process_start_game(message: Message):
    if not users[message.from_user.id].in_game:
        users[message.from_user.id].in_game = True
        users[message.from_user.id].secret_num = random.randint(1, 100)
        users[message.from_user.id].attempts = ATTEMPTS
        await message.answer('Я загадал число от 1 до 100\nПопробуй его отгадать')
    else:
        await message.answer('Мы уже играем!')


@dp.message(lambda x: x.text and x.text.isdigit())
async def process_num_answer(message: Message):
    if users[message.from_user.id].in_game:
        player_num = int(message.text)
        if 1 <= player_num <= 100:
            users[message.from_user.id].attempts-= 1
            if player_num == users[message.from_user.id].secret_num:
                users[message.from_user.id].in_game = False
                users[message.from_user.id].total_played += 1
                users[message.from_user.id].wins += 1
                await message.answer('Поздравляю, ты угадал!\nХочешь сыграть ещё?')
            elif player_num > users[message.from_user.id].secret_num:
                await message.answer('Число которое я загадал меньше')
            else:
                await message.answer('Число которое я загадал больше')
        else:
            await message.answer('Число, загаданное мной, находится в диапозоне [1, 100]')

        if users[message.from_user.id].attempts == 0:
            users[message.from_user.id].in_game = False
            users[message.from_user.id].total_played += 1
            await message.answer(
                f'К сожалению у тебя закончились попытки(\n'
                f'Я загадал число {users[message.from_user.id].secret_num}\n'
                'Хочешь сыграть ещё?'
            )
    else:
        await message.answer('Мы ещё не играем')


@dp.message(F.text.lower().in_(['киска', 'собачка', 'лисичка']))
async def send_animal(message: Message):
    url = eval('requests.get' + animals[message.text.lower()])
    await message.answer_photo(photo=url)

if __name__ == '__main__':
    dp.run_polling(bot)