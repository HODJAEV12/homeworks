# Я прокоментировал код, чтобы он выглядел красивее и читабельнее

# ----- ИМПОРТЫ -----

import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ----- БОТ -----

TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# ----- СОЗДАНИЕ БД И ТАБЛИЦЫ -----

conn = sqlite3.connect("tasks.db")
cur = conn.cursor()

cur.execute("""
create table if not exists tasks (
    id integer primary key autoincrement,
    telegram_id integer,
    title text,
    description text
)
""")
conn.commit()

# ----- FSM КЛАССЫ -----

class AddTask(StatesGroup):
    title = State()
    description = State()

class EditTask(StatesGroup):
    task_id = State()
    description = State()

# ----- МЕНЮ -----

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task")],
            [InlineKeyboardButton(text="📝 Мои задачи", callback_data="my_tasks")],
            [InlineKeyboardButton(text="✏️ Изменить задачу", callback_data="edit_task")],
            [InlineKeyboardButton(text="❌ Удалить задачу", callback_data="delete_task")],
        ]
    )

# ----- СТАРТ -----

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("<b>👋 Привет! Это твой бот, который хранит твои задачи</b>", reply_markup=main_menu())

# ----- ДОБАВЛЕНИЕ ЗАДАЧИ -----

@dp.callback_query(F.data == "add_task")
async def add(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("✏️ Введите заголовок задачи:")
    await state.set_state(AddTask.title)

@dp.message(AddTask.title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("✏️ Введите текст заметки:")
    await state.set_state(AddTask.description)

@dp.message(AddTask.description)
async def get_description(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    description = message.text
    telegram_id = message.from_user.id

    cur.execute("insert into tasks (telegram_id, title, description) values (?, ?, ?)", (telegram_id, title, description))
    conn.commit()

    await state.clear()
    await message.answer(f"✅ Задача сохранена.\n\n<b>{title}</b>\n{description}", reply_markup=main_menu())

# ----- ПРОСМОТР ЗАДАЧ -----

@dp.callback_query(F.data == "my_tasks")
async def show_tasks(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    cur.execute("select id, title, description from tasks where telegram_id = ?", (telegram_id,))
    tasks = cur.fetchall()

    if not tasks:
        await callback.answer("❌ У вас пока нет задач.")
        return

    text = "<b>📝 Ваши задачи:</b>\n\n"
    for note_id, title, note_text in tasks:
        text += f"ID: {note_id}\n<b>{title}</b>\n{note_text}\n--------------------\n"

    await callback.answer()
    await callback.message.answer(text, reply_markup=main_menu())

# ----- ИЗМЕНЕНИЕ ЗАДАЧИ -----

@dp.callback_query(F.data == "edit_task")
async def show_buttons(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    cur.execute("select id, title from tasks where telegram_id = ?", (telegram_id,))
    tasks = cur.fetchall()

    if not tasks:
        await callback.answer("❌ У вас нет задач для изменения.")
        return

    for task_id, title in tasks:
        buttons = [ [ InlineKeyboardButton(text=title, callback_data=f"edit:{task_id}") ] ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.answer()
    await callback.message.answer("Выберите задачу, которую хотите изменить:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("edit:"))
async def choose_task(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split(":")[1])
    await state.update_data(task_id=task_id)
    await callback.answer()
    await callback.message.answer("✏️ Введите новый текст задачи:")
    await state.set_state(EditTask.description)

@dp.message(EditTask.description)
async def update_task(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data["task_id"]
    telegram_id = message.from_user.id
    new_description = message.text

    cur.execute("update tasks set description = ? where id = ? and telegram_id = ?", (new_description, task_id, telegram_id))
    conn.commit()

    await state.clear()

    if cur.rowcount == 0:
        await message.answer("❌ Задача не найдена.")
        return

    await message.answer("✅ Задача успешно изменена.", reply_markup=main_menu())

# ----- УДАЛЕНИЕ ЗАДАЧИ -----

@dp.callback_query(F.data == "delete_task")
async def show_buttons(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    cur.execute("select id, title from tasks where telegram_id = ?", (telegram_id,))
    tasks = cur.fetchall()

    if not tasks:
        await callback.answer("❌ У вас нет задач для удаление.")
        return

    for task_id, title in tasks:
        buttons = [ [ InlineKeyboardButton(text=title, callback_data=f"delete:{task_id}") ] ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.answer()
    await callback.message.answer("👆 Выберите задачу, которую хотите удалить:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("delete:"))
async def delete_task(callback : CallbackQuery):
    task_id = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    cur.execute("delete from tasks where id = ? and telegram_id = ?", (task_id, telegram_id,))
    conn.commit()

    if cur.rowcount == 0:
        await callback.answer("❌ Задача не найдена.")
        return
    
    await callback.answer()
    await callback.message.answer("✅ Задача успешно удалена." ,reply_markup=main_menu())

# ----- ПОМОЩЬ -----

@dp.message()
async def unknown(message : Message):
    await message.answer("Такая команда не найдена!")
    await message.answer("Напиши /help для помощи")

@dp.message(F.text == "/help")
async def unknown(message : Message):
    await message.answer("▶️/start - меню\n🆘/help - помощь")

# ----- ЗАПУСК -----

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        conn.close()