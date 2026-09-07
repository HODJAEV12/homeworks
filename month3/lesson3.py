###### Викторины, Callback и FSM

# InlineKeyboard
# InlineKeyboardMarkup - InlineKeyboardButton 

### Создание кнопок

# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types import CallbackQuery

# keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text="Python",
#                 callback_data="python"
#             )
#         ]
#     ]
# )

# @dp.callback_query(F.data == "python")
# async def python_callback(callback : CallbackQuery):
#     await callback.message.answer("Вы выбрали python!")

# Викторина

# import asyncio
# from aiogram import Bot, Dispatcher, F
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types import CallbackQuery, Message

# TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"
# bot = Bot(token=TOKEN)
# dp = Dispatcher()

# @dp.message(F.text == "/start")
# async def start(message: Message):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Python", callback_data="python")],
#             [InlineKeyboardButton(text="Java", callback_data="java")],
#             [InlineKeyboardButton(text="C++", callback_data="c++")]
#         ]
#     )
#     await message.answer("На каком языке написан фреймворк Django?", reply_markup=keyboard)

# @dp.callback_query(F.data == "python")
# async def correct_answer(callback: CallbackQuery):
#     await callback.answer("Правильно!")
#     await callback.message.answer("Правильный ответ! Django написан на Python.")

# @dp.callback_query(F.data == "java")
# async def java_answer(callback: CallbackQuery):
#     await callback.answer("Неправильно!")
#     await callback.message.answer("Нет! Django написан на Python.")

# @dp.callback_query(F.data == "c++")
# async def cpp_answer(callback: CallbackQuery):
#     await callback.answer("Неправильно!")
#     await callback.message.answer("Нет! Django написан на Python.")

# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())

### FSM - Finite State Machine - Конечный автомат

import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Registration(StatesGroup):
    name = State()
    age = State()

@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):

    await message.answer(
        "Привет! Давай зарегистрируемся.\n"
        "Как тебя зовут?"
    )

    await state.set_state(Registration.name)

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer(
        "Отлично!\n"
        "Сколько тебе лет?"
    )

    await state.set_state(Registration.age)

@dp.message(Registration.age)
async def get_age(message: Message, state: FSMContext):

    await state.update_data(age=message.text)

    data = await state.get_data()

    await message.answer(
        f"Регистрация завершена!\n\n"
        f"Имя: {data ['name']}\n"
        f"Возраст: {data ['age']}"
    )

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())