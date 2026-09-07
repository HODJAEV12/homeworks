# Я прокоментировал код, чтобы он выглядел читабельнее и красивее

# ----- ИМПОРТЫ -----

import asyncio
import sqlite3
from token_ import token
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

# ----- БОТ -----

TOKEN = token
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# ----- КОННЕКТ С БД -----

connect = sqlite3.connect("timetable.db")
cursor = connect.cursor()

# ----- СОЗДАНИЕ БД ТАБЛИЦЫ -----

cursor.execute("""
create table if not exists timetable (
    id integer primary key autoincrement,
    telegram_id integer,
    week_day text,
    subject text,
    time time,
    cabinet text
)
""")
connect.commit()

# ----- FSM КЛАСС -----

class AddTimetable(StatesGroup):
    week_day = State()
    subject = State()
    time = State()
    cabinet = State()

# ----- МЕНЮ ----

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [ InlineKeyboardButton(text="➕ Добавить занятие", callback_data="add_lesson") ],
            [ InlineKeyboardButton(text="🔎 Показать расписание", callback_data="show_timetable") ],
            [ InlineKeyboardButton(text="👆 Выбрать день", callback_data="choose_day") ],
            [ InlineKeyboardButton(text="🗑 Удалить занятие", callback_data="delete_lesson") ]
        ]
    )

# ----- СТАРТ -----

@dp.message(F.text == "/start")
async def start(message : Message):
    await message.answer("<b>👋 HI! Я твой Telegram-бот хранящий расписание</b>", reply_markup=main_menu())

# ----- ДОБАВЛЕНИЕ РАСПИСАНИЯ -----

@dp.callback_query(F.data == "add_lesson")
async def get_weekday(callback : CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.answer("<b>🗓 Введите день недели:</b>")
    await state.set_state(AddTimetable.week_day)

@dp.message(AddTimetable.week_day)
async def get_subject(message : Message, state : FSMContext):
    await state.update_data(week_day=message.text)
    await message.answer("<b>🎓 Введите предмет</b>:")
    await state.set_state(AddTimetable.subject)

@dp.message(AddTimetable.subject)
async def get_time(message : Message, state : FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("<b>🕓 Введите время(ЧЧ:ММ:CC)</b>:")
    await state.set_state(AddTimetable.time)

@dp.message(AddTimetable.time)
async def get_canibet(message : Message, state : FSMContext):
    await state.update_data(time=message.text)
    await message.answer("<b>#️⃣ Введите номер кабинета</b>:")
    await state.set_state(AddTimetable.cabinet)

@dp.message(AddTimetable.cabinet)
async def add_timetbale(message : Message, state : FSMContext):
    data = await state.get_data()

    week_day = data["week_day"]
    subject = data["subject"]
    time = data["time"]
    cabinet = message.text
    telegram_id = message.from_user.id

    cursor.execute("insert into timetable(telegram_id, week_day, subject, time, cabinet) values(?, ?, ?, ?, ?)", 
    (telegram_id, week_day, subject, time, cabinet))
    connect.commit()

    await state.clear()
    await message.answer(
        f"<b>✅ Расписание сохранено.</b>\n\n"
        f"<b>🗓 День недели:</b> {week_day}\n"
        f"<b>🎓 Предмет:</b> {subject}\n"
        f"<b>🕓 Время:</b> {time}\n"
        f"<b>#️⃣ Кабинет:</b> {cabinet}\n",
        reply_markup=main_menu()
    )

# ----- ПОКАЗ РАСПИСАНИЯ -----

@dp.callback_query(F.data == "show_timetable")
async def show_timetable(callback : CallbackQuery):
    telegram_id = callback.from_user.id

    cursor.execute("select id, week_day, subject, time, cabinet from timetable where telegram_id = ?", (telegram_id,))
    lessons = cursor.fetchall()

    if not lessons:
        await callback.answer()
        await callback.message.answer("❌ Данных нет.", reply_markup=main_menu())
        return

    text = "<b>------- 🗓 РАСПИСАНИЕ -------</b>\n"

    for lesson in lessons:
        lesson_id, week_day, subject, time, cabinet = lesson

        text += (
            f"<b>🆔 ID:</b> {lesson_id}\n"
            f"<b>🗓 День недели:</b> {week_day}\n"
            f"<b>🎓 Предмет:</b> {subject}\n"
            f"<b>🕓 Время:</b> {time}\n"
            f"<b>#️⃣ Кабинет:</b> {cabinet}\n"
            "--------------------------\n"
        )

    await callback.answer()
    await callback.message.answer(text, reply_markup=main_menu())

# ----- ВЫБОР ДНЯ -----

@dp.callback_query(F.data == "choose_day")
async def choose_day(callback : CallbackQuery):
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1️⃣ Понедельник", callback_data="day:Понедельник"),
                InlineKeyboardButton(text="2️⃣ Вторник", callback_data="day:Вторник")
            ],
            [
                InlineKeyboardButton(text="3️⃣ Среда", callback_data="day:Среда"),
                InlineKeyboardButton(text="4️⃣ Четверг", callback_data="day:Четверг")
            ],
            [
                InlineKeyboardButton(text="5️⃣ Пятница", callback_data="day:Пятница"),
                InlineKeyboardButton(text="6️⃣ Суббота", callback_data="day:Суббота")
            ],
            [ InlineKeyboardButton(text="7️⃣ Воскресенье", callback_data="day:Воскресенье") ]
        ]
    )

    await callback.answer()
    await callback.message.answer("<b>🗓 Выберите день недели:</b>", reply_markup=buttons)

@dp.callback_query(F.data.startswith("day:"))
async def get_day(callback : CallbackQuery):
    day = callback.data.split(":")[1]

    cursor.execute("select subject, time from timetable where week_day = ? order by time", (day,))
    subjects = cursor.fetchall()

    if not subjects:
        await callback.answer()
        await callback.message.answer("❌ Данных нет.", reply_markup=main_menu())
        return

    text = f"<b>🎓 Уроки на {day}:</b>\n"

    for subject, time in subjects:
        text += f"{subject} - {time}\n"

    await callback.answer()
    await callback.message.answer(text, reply_markup=main_menu())

# ----- УДАЛЕНИЕ ЗАНЯТИЯ -----

@dp.callback_query(F.data == "delete_lesson")
async def choose_lesson(callback: CallbackQuery):
    cursor.execute("select id, week_day, subject, time from timetable order by time")
    lessons = cursor.fetchall()

    if not lessons:
        await callback.answer()
        await callback.message.answer("❌ Нет данных.")
        return

    buttons = []
    for lesson_id, day, subject, time in lessons:
        btn_text = f"❌ {day} | {time} - {subject}"
        buttons.append( [ InlineKeyboardButton(text=btn_text, callback_data=f"delete:{lesson_id}") ] )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.answer()
    await callback.message.answer("🗑 Выберите занятие, которое нужно удалить:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("delete:"))
async def delete_lesson(callback: CallbackQuery):
    lesson_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    cursor.execute("delete from timetable where id = ? and telegram_id = ?", (lesson_id, telegram_id))
    connect.commit()

    await callback.answer("")
    await callback.message.edit_text("🗑 Занятие успешно удалено из расписания.")

# ----- ПОМОЩЬ -----

@dp.message(F.text == "/help")
async def unknown(message : Message):
    await message.answer("▶️ /start - меню\n🆘 /help - помощь")

# ----- ЗАПУСК БОТА -----

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try: asyncio.run(main())
    finally: connect.close()