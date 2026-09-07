from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio

TOKEN = "8861244057:AAHQu9SXwCtifvIyDTEa4UwtDIdvqviXwLg"
bot = Bot( token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML) )
dp = Dispatcher()

@dp.message(F.text == "Привет")
async def hello(message : Message):
    await message.answer("Привет!")

@dp.message(F.text == "Кто ты?")
async def who_are_you(message : Message):
    await message.answer("Я твой Телеграм-бот.")

@dp.message(F.text == "Сколько команд знаешь?")
async def commands_count(message : Message):
    await message.answer("Я знаю 5 команд.")

@dp.message(F.text == "Какой у тебя токен?")
async def token(message : Message):
    await message.answer(f"Мой токен --> '{TOKEN}'")

@dp.message(F.text == "Пока")
async def bye(message : Message):
    await message.answer("Пока. Еще увидимся!")

@dp.message()
async def unknown(message : Message):
    await message.answer("Извините, я пока не умею отвечать на такие сообщения.")

async def main(): 
    await dp.start_polling(bot)

if __name__ == "__main__": 
    asyncio.run(main())