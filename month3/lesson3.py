import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery, Message

TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def instriction(message: Message):
    await message.answer("1 - первый вопрос\n2 - второй вопрос\n3 - третий вопрос")

# ------------------ ПЕРВЫЙ ВОПРОС ------------------

@dp.message(F.text == "1")
async def question1(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Cristiano Ronaldo", callback_data="ronaldo")],
            [InlineKeyboardButton(text="Lionel Messi", callback_data="messi")],
            [InlineKeyboardButton(text="Neymar Jr", callback_data="neymar")]
        ]
    )
    await message.answer("Какой футболист забил больше всего голов?", reply_markup=keyboard)

@dp.callback_query(F.data == "ronaldo")
async def ronaldo_question1(callback : CallbackQuery):
    await callback.answer("Правильно! ✅")
    await callback.message.answer("✅ Правильно! Ronaldo лучший бомбардир!")


@dp.callback_query(F.data == "messi")
async def messi_question1(callback : CallbackQuery):
    await callback.answer("Неравильно! ❌")
    await callback.message.answer("❌ Неправильно! Ronaldo лучший бомбардир!")


@dp.callback_query(F.data == "neymar")
async def neymar_question1(callback : CallbackQuery):
    await callback.answer("Неправильно! ❌")
    await callback.message.answer("❌ Неправильно! Ronaldo лучший бомбардир!")

# ------------------ ВТОРОЙ ВОПРОС ------------------

@dp.message(F.text == "2")
async def question2(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Rockstar Games", callback_data="rockstar")],
            [InlineKeyboardButton(text="EA Sports", callback_data="ea")],
            [InlineKeyboardButton(text="Valve", callback_data="valve")]
        ]
    )
    await message.answer("Какая компания выпустила игру CS2?", reply_markup=keyboard)

@dp.callback_query(F.data == "valve")
async def valve_question2(callback : CallbackQuery):
    await callback.answer("Правильно! ✅")
    await callback.message.answer("✅ Правильно! CS2 выпустила Valve!")


@dp.callback_query(F.data == "ea")
async def ea_questio2(callback : CallbackQuery):
    await callback.answer("Неравильно! ❌")
    await callback.message.answer("❌ Неправильно! CS2 выпустила Valve!")


@dp.callback_query(F.data == "rockstar")
async def rockstar_question2(callback : CallbackQuery):
    await callback.answer("Неправильно! ❌")
    await callback.message.answer("Ds❌ Неправильно! CS2 выпустила Valve!")

# ------------------ ТРЕТИЙ ВОПРОС ------------------

@dp.message(F.text == "3")
async def question3(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вьетнам", callback_data="vietnam")],
            [InlineKeyboardButton(text="Непал", callback_data="nepal")],
            [InlineKeyboardButton(text="Китай", callback_data="china")]
        ]
    )
    await message.answer("В какой стране находится Эверест?", reply_markup=keyboard)

@dp.callback_query(F.data == "nepal")
async def nepal_question2(callback : CallbackQuery):
    await callback.answer("Правильно! ✅")
    await callback.message.answer("✅ Правильно! Эверест находится в Непале!")


@dp.callback_query(F.data == "vietnam")
async def vietnam_questio2(callback : CallbackQuery):
    await callback.answer("Неравильно! ❌")
    await callback.message.answer("❌ Неправильно! Эверест находится в Непале!")


@dp.callback_query(F.data == "china")
async def china_question2(callback : CallbackQuery):
    await callback.answer("Неправильно! ❌")
    await callback.message.answer("❌ Неправильно! Эверест находится в Непале!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())