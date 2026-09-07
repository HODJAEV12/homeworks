###### SQL и базы данных. Часть 1: проектирование и связи

# import asyncio
# import sqlite3
# from aiogram import Bot, Dispatcher, F
# from aiogram.types import Message, CallbackQuery
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"
# bot = Bot(token=TOKEN)
# dp = Dispatcher()

# connection = sqlite3.connect("lesson4.db")
# cursor = connection.cursor()

# cursor.execute("""
# create table if not exists students (
#     id integer primary key autoincrement,
#     telegram_id integer,
#     name text not null
# )
# """)

# @dp.message(F.text == "/start")
# async def start(message : Message):
#     await message.answer("Привет! Как тебя зовут?")

# @dp.message()
# async def save_student(message : Message):
#     name = message.text
#     cursor.execute("insert into students(telegram_id, name) values(?, ?)", (message.from_user.id, name))
#     await message.answer(f"Приятно познакомиться, {name}! Я сохранил тебя в БД.")

# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())

# connection.commit()
# connection.close()



import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message


TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name TEXT NOT NULL,
        age INTEGER,
        city TEXT
    )
""")

conn.commit()


@dp.message(F.text == "/start")
async def start(message: Message):

    telegram_id = message.from_user.id
    name = message.from_user.first_name

    cur.execute(
        """
        SELECT * FROM students
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    student = cur.fetchone()

    if student:
        await message.answer(
            f"👋🏼 С возвращением, {name}!\n\n"
            "Ты уже есть в базе данных.\n\n"
            "Команды:\n"
            "/me - мой профиль\n"
            "/students - список студентов\n"
            "/help - помощь"
        )

    else:
        cur.execute(
            """
            INSERT INTO students (telegram_id, name)
            VALUES (?, ?)
            """,
            (telegram_id, name)
        )

        conn.commit()

        await message.answer(
            f"👋🏼 Привет, {name}!\n\n"
            "Ты зарегистрирован и сохранён в базе данных.\n\n"
            "Команды:\n"
            "/me - мой профиль\n"
            "/students - список студентов\n"
            "/help - помощь"
        )


@dp.message(F.text == "/me")
async def my_profile(message: Message):

    telegram_id = message.from_user.id

    cur.execute(
        """
        SELECT id, name, age, city
        FROM students
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    student = cur.fetchone()

    if not student:
        await message.answer(
            "❌ Ты ещё не зарегистрирован.\n"
            "Напиши /start"
        )
        return

    student_id, name, age, city = student

    age = age if age else "Не указан"
    city = city if city else "Не указан"

    await message.answer(
        f"👤 Твой профиль\n\n"
        f"ID: {student_id}\n"
        f"Имя: {name}\n"
        f"Возраст: {age}\n"
        f"Город: {city}"
    )


@dp.message(F.text == "/students")
async def students(message: Message):

    cur.execute(
        """
        SELECT id, name, age, city
        FROM students
        """
    )

    students_list = cur.fetchall()

    if not students_list:
        await message.answer("В базе пока нет студентов.")
        return

    text = "🧑🏼‍🎓 Студенты:\n\n"

    for student in students_list:

        student_id, name, age, city = student

        age = age if age else "Не указан"
        city = city if city else "Не указан"

        text += (
            f"ID: {student_id}\n"
            f"Имя: {name}\n"
            f"Возраст: {age}\n"
            f"Город: {city}\n"
            "——————————————————\n"
        )

    await message.answer(text)


@dp.message(F.text == "/help")
async def help_command(message: Message):

    await message.answer(
        "📚 Команды бота\n\n"
        "/start — регистрация\n"
        "/me — мой профиль\n"
        "/students — все студенты\n"
        "/help — помощь"
    )


@dp.message()
async def unknown(message: Message):

    await message.answer(
        "❓ Я не знаю такую команду.\n\n"
        "Используй /help"
    )


async def main():

    print("🤖 Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "main":

    try:
        asyncio.run(main())

    finally:
        conn.close()