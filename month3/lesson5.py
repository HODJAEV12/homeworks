##### SQL и CRUD. Часть 2: SELECT, INSERT, UPDATE, DELETE

import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher(
    storage=MemoryStorage()
)


conn = sqlite3.connect("notes.db")
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL
)
""")

conn.commit()


class AddNote(StatesGroup):
    title = State()
    text = State()


class EditNote(StatesGroup):
    note_id = State()
    text = State()


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить заметку",
                    callback_data="add_note"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Мои заметки",
                    callback_data="my_notes"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Изменить заметку",
                    callback_data="edit_note"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Удалить заметку",
                    callback_data="delete_note"
                )
            ]
        ]
    )


@dp.message(F.text == "/start")
async def start(message: Message):

    await message.answer(
        "<b>Мои заметки</b>\n\n"
        "Здесь Вы можете создавать и хранить свои заметки.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "add_note")
async def add_note_start(
    callback: CallbackQuery,
    state: FSMContext
):

    await callback.answer()

    await callback.message.answer(
        "Добавление новой заметки.\n\n"
        "Введите название заметки:"
    )

    await state.set_state(AddNote.title)


@dp.message(AddNote.title)
async def get_note_title(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        title=message.text
    )

    await message.answer(
        "Введите текст заметки:"
    )

    await state.set_state(AddNote.text)


@dp.message(AddNote.text)
async def get_note_text(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    title = data["title"]
    text = message.text

    telegram_id = message.from_user.id

    cur.execute(
        """
        INSERT INTO notes
        (telegram_id, title, text)
        VALUES (?, ?, ?)
        """,
        (
            telegram_id,
            title,
            text
        )
    )

    conn.commit()

    await state.clear()

    await message.answer(
        "Заметка сохранена.\n\n"
        f"<b>{title}</b>\n"
        f"{text}",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "my_notes")
async def my_notes(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    cur.execute(
        """
        SELECT id, title, text
        FROM notes
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    notes = cur.fetchall()

    if not notes:

        await callback.answer()

        await callback.message.answer(
            "У Вас пока нет заметок.",
            reply_markup=main_menu()
        )

        return

    text = "<b>Ваши заметки:</b>\n\n"

    for note in notes:

        note_id, title, note_text = note

        text += (
            f"ID: {note_id}\n"
            f"<b>{title}</b>\n"
            f"{note_text}\n"
            "--------------------\n"
        )

    await callback.answer()

    await callback.message.answer(
        text,
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "edit_note")
async def edit_note_start(
    callback: CallbackQuery,
    state: FSMContext
):

    telegram_id = callback.from_user.id

    cur.execute(
        """
        SELECT id, title
        FROM notes
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    notes = cur.fetchall()

    if not notes:

        await callback.answer(
            "У Вас нет заметок."
        )

        return

    buttons = []

    for note_id, title in notes:

        buttons.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"edit:{note_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.answer()

    await callback.message.answer(
        "Выберите заметку, которую хотите изменить:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data.startswith("edit:"))
async def choose_note(
    callback: CallbackQuery,
    state: FSMContext
):

    note_id = int(
        callback.data.split(":")[1]
    )

    await state.update_data(
        note_id=note_id
    )

    await callback.answer()

    await callback.message.answer(
        "Введите новый текст заметки:"
    )

    await state.set_state(
        EditNote.text
    )


@dp.message(EditNote.text)
async def update_note(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    note_id = data["note_id"]

    telegram_id = message.from_user.id

    new_text = message.text

    cur.execute(
        """
        UPDATE notes
        SET text = ?
        WHERE id = ?
        AND telegram_id = ?
        """,
        (
            new_text,
            note_id,
            telegram_id
        )
    )

    conn.commit()

    await state.clear()

    if cur.rowcount == 0:

        await message.answer(
            "Заметка не найдена."
        )

        return

    await message.answer(
        "Заметка изменена.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "delete_note")
async def delete_note_start(
    callback: CallbackQuery
):

    telegram_id = callback.from_user.id

    cur.execute(
        """
        SELECT id, title
        FROM notes
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    notes = cur.fetchall()

    if not notes:

        await callback.answer(
            "У Вас нет заметок."
        )

        return

    buttons = []

    for note_id, title in notes:

        buttons.append([
            InlineKeyboardButton(
                text=title,
                callback_data=f"delete:{note_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.answer()

    await callback.message.answer(
        "Выберите заметку для удаления:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data.startswith("delete:"))
async def delete_note(
    callback: CallbackQuery
):

    note_id = int(
        callback.data.split(":")[1]
    )

    telegram_id = callback.from_user.id

    cur.execute(
        """
        DELETE FROM notes
        WHERE id = ?
        AND telegram_id = ?
        """,
        (
            note_id,
            telegram_id
        )
    )

    conn.commit()

    if cur.rowcount == 0:

        await callback.answer(
            "Заметка не найдена."
        )

        return

    await callback.answer()

    await callback.message.answer(
        "Заметка удалена.",
        reply_markup=main_menu()
    )


@dp.message(F.text == "/help")
async def help_command(message: Message):

    await message.answer(
        "<b>Мои заметки</b>\n\n"
        "/start — открыть меню\n"
        "/help — помощь"
    )


async def main():

    print("Notes Bot запущен.")

    await dp.start_polling(bot)


if __name__ == "__main__":

    try:
        asyncio.run(main())

    finally:
        conn.close()