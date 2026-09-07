###### Знакомство с Telegram-ботами и библиотекой aiogram

# from aiogram import Bot, Dispatcher
# from aiogram.enums import ParseMode
# from aiogram.client.default import DefaultBotProperties
# import asyncio

# TOKEN = "8643500356:AAHGHgsGQg0NUDr8hexB1RxloeM3IuST1NE"

# bot = Bot(
#     token=TOKEN,
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )

# dp = Dispatcher()

# async def main():
#     await dp.start_polling(bot)

# if __name__ == '__main__':
#     asyncio.run(main())



from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
import asyncio

TOKEN = "8643500356:AAHGHgsGQg0NUDr8hexB1RxloeM3IuST1NE"

bot = Bot( token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML) )

dp = Dispatcher()

@dp.message(F.text == "Привет")
async def hello(message : Message):
    await message.answer("Привет! Я твой Телеграм-бот.")

@dp.message(F.text == "Как дела?")
async def how_are_you(message : Message):
    await message.answer("Отлично! А у тебя?")

@dp.message()
async def unknown(message : Message):
    await message.answer("Я пока не понимаю эту команду.")

async def main(): 
    await dp.start_polling(bot)

if __name__ == "__main__": 
    asyncio.run(main())