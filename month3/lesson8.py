# ------ ГЕНЕРАТОР ПАРОЛЕЙ ------

# ------ ИМПОРТЫ ------

import asyncio
import sqlite3
import random
from token_ import token # импортировал токен через другой python файл
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

# ------ БОТ ------

TOKEN = token
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# ------ КОННЕКТ С БД ------

connect = sqlite3.connect("passwords.db")
cursor = connect.cursor()

# ------ СОЗДАНИЕ БД ТАБЛИЦЫ ------

cursor.execute("""
create table if not exists passwords (
    id integer primary key autoincrement,
    telegram_id integer,
    password text
)
""")

# ------ FSM КЛАСС ------

class GeneratePassword(StatesGroup):
    length = State()

# ------ МЕНЮ ------

def menu():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [ InlineKeyboardButton(text="➕ Сгенерировать пароль", callback_data="generate") ],
            [ InlineKeyboardButton(text="🔑 Все пароли", callback_data="show_passwords") ],
            [ InlineKeyboardButton(text="🗑 Удалить пароль", callback_data="delete") ]
        ]
    )

# ------ СТАРТ ------

@dp.message(F.text == "/start")
async def start(message : Message, state : FSMContext):
    await message.answer("<b>👋 Привет! Это генератор паролей.</b>", reply_markup=menu())

# ------ ГЕНЕРАЦИЯ ПАРОЛЯ ------

@dp.callback_query(F.data == "generate")
async def get_length(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer("<b>Введите длину пароля:</b>")
    await state.set_state(GeneratePassword.length)

@dp.message(GeneratePassword.length)
async def generate_password(message : Message, state : FSMContext):
    telegram_id = message.from_user.id
    
    length = int(message.text)
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    specials = "~!@#$%^&*()._?/;:"

    random_chars = random.choices(chars, k=length)
    random_numbers = random.choices(numbers, k=length)
    random_specials = random.choices(specials, k=length)

    all_symbols = random_chars + random_numbers + random_specials

    generated_password = random.choices(all_symbols, k=length)
    generated_password = "".join(generated_password)

    cursor.execute("insert into passwords(telegram_id, password) values(?, ?)", (telegram_id, generated_password))
    connect.commit()

    await message.answer(
        f"<b>✅ Ваш сгенерированный пароль успешно сохранён.</b>\nПароль: {generated_password}", reply_markup=menu()
    )

# ------ ВСЕ ПАРОЛИ ------

@dp.callback_query(F.data == "show_passwords")
async def show_passwords(callback : CallbackQuery):
    telegram_id = callback.from_user.id

    cursor.execute("select password from passwords where telegram_id = ?", (telegram_id,))
    passwords = cursor.fetchall()

    if not passwords:
        await callback.answer()
        await callback.message.answer("❌ Нет данных.", reply_markup=menu())
        return

    text = "<b>🔑 Пароли:</b>\n"
    count = 0

    for password in passwords:
        count += 1
        text += f"{count}. {password[0]}\n"

    await callback.answer()
    await callback.message.answer(text, reply_markup=menu())
        

# ------ УДАЛЕНИЕ ПАРОЛЯ ------

@dp.callback_query(F.data == "delete")
async def choose_password(callback : CallbackQuery):
    telegram_id = callback.from_user.id

    cursor.execute("select id, password from passwords where telegram_id = ?", (telegram_id,))
    passwords = cursor.fetchall()

    if not passwords:
        await callback.answer()
        await callback.message.answer("❌ Нет данных.")
        return

    buttons = []

    for password_id, password in passwords:
        buttons.append( [ InlineKeyboardButton(text=password, callback_data=f"delete:{password_id}") ] )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.answer()
    await callback.message.answer("<b>Выберите пароль, который хотите удалить:</b>", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("delete:"))
async def delete_task(callback : CallbackQuery):
    password_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    cursor.execute("delete from passwords where id = ? and telegram_id = ?", (password_id, telegram_id,))
    connect.commit()
    
    await callback.answer()
    await callback.message.answer("✅ Пароль успешно удалён." ,reply_markup=menu())

# ----- ПОМОЩЬ -----

@dp.message()
async def help(message : Message):
    await message.answer("Такая команда не найдена!")
    await message.answer("▶️/start - меню\n🆘/help - помощь")

# ------ ЗАПУСК БОТА ------

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try: asyncio.run(main())
    finally: connect.close()