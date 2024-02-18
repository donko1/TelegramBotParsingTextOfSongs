
import sys
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Filter
from parser import parse

try:
    with open("config.json", "r") as file:
        config_data = json.load(file)
        token = config_data.get("token")
        if token:
            print("Token:", token)
        else:
            print("Файл config.json не содержит необходимых данных")
except FileNotFoundError:
    print("Файл config.json не найден")
    sys.exit(1)
except json.JSONDecodeError:
    print("Ошибка при чтении данных из файла config.json")
    sys.exit(1)


API_TOKEN = token
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.my_text

@dp.message(MyFilter("/start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот, готовый помочь вам найти текст руской песни 90-ых и 00-ых! Просто напиши мне название песни без исполнителя!")

@dp.message()
async def reply_to_message(message: types.Message):
    text_song = parse(message.text)
    await message.answer(text_song)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

