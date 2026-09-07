import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        city TEXT,
        street TEXT,
        phone TEXT
    )
"""
)
conn.commit()


@dp.message(F.text == "/start")
async def start_cmd(message: Message):
    tg_id = message.from_user.id
    first_name = message.from_user.first_name or "Не указано"
    last_name = message.from_user.last_name or "Не указано"

    cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (tg_id,))
    if cursor.fetchone():
        await message.answer(
            "Вы уже в базе! Напишите /me для просмотра профиля."
        )
        return

    cursor.execute(
        """
        INSERT INTO users (telegram_id, first_name, last_name, age, city, street, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (tg_id, first_name, last_name, 14, "Ош", "Ахмедова", "+996550909800"),
    )
    conn.commit()

    await message.answer("Вы успешно добавлены в базу данных!")


@dp.message(F.text == "/me")
async def me_cmd(message: Message):
    cursor.execute(
        "SELECT id, telegram_id, first_name, last_name, age, city, street, phone FROM users WHERE telegram_id = ?",
        (message.from_user.id,),
    )
    user = cursor.fetchone()

    if not user:
        await message.answer("Вас нет в базе. Введите /start.")
        return

    text = (
        f"ID в БД: {user[0]}\n"
        f"Telegram ID: {user[1]}\n"
        f"Имя: {user[2]}\n"
        f"Фамилия: {user[3]}\n"
        f"Возраст: {user[4]}\n"
        f"Город: {user[5]}\n"
        f"Улица: {user[6]}\n"
        f"Телефон: {user[7]}"
    )
    await message.answer(text)

@dp.message(F.text == "/users")
async def users_cmd(message: Message):
    cursor.execute(
        "SELECT id, telegram_id, first_name, last_name, age, city, street, phone FROM users"
    )
    users = cursor.fetchall()

    if not users:
        await message.answer("База данных пуста.")
        return

    text = "Все пользователи:\n\n"
    for u in users:
        text += f"ID: {u[0]} | TG: {u[1]} | {u[2]} {u[3]} | {u[4]} лет | г. {u[5]}, ул. {u[6]} | тел: {u[7]}\n"

    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())