##### JOIN — связываем таблицы. Фильтрация данных, WHERE, GROUP BY, HAVING, COUNT

# WHERE - фильтрует отдельные строки
# GROUP BY - объединяет одинаковые значения в группы
# HAVING - нужен для фильрации групп
# COUNT - считает количество записей

import asyncio
import sqlite3
from token_ import token
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = token

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

conn = sqlite3.connect("courses.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.executescript("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS student_course (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
""")
conn.commit()


def keyboard(*rows):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t, callback_data=d) for t, d in row]
            for row in rows
        ]
    )


def main_menu():
    return keyboard(
        (("📚 Список курсов", "courses"),),
        (("👨‍🎓 Студенты курса", "course_students"),),
        (("🔥 Популярные курсы", "popular"),),
        (("👥 Все студенты", "students"),),
        (("⚙️ Управление", "manage"),),
    )


def manage_menu():
    return keyboard(
        (("➕ Добавить курс", "add_course_help"),),
        (("➕ Добавить студента", "add_student_help"),),
        (("🔗 Записать на курс", "enroll_help"),),
        (("❌ Удалить курс", "delete_course"),),
        (("❌ Удалить студента", "delete_student"),),
        (("🔗 Убрать с курса", "unenroll"),),
        (("⬅️ Главное меню", "main_menu"),),
    )


async def send_main(message: Message, text: str):
    await message.answer(text, reply_markup=main_menu())


@dp.message(F.text == "/start")
async def start(message: Message):
    await send_main(message, "<b>📚 Курсы</b>\n\nВыберите нужный раздел:")


@dp.message(F.text == "/help")
async def help_command(message: Message):
    await message.answer(
        "<b>📚 Курсы — помощь</b>\n\n"
        "<b>Добавление:</b>\n"
        "/add_course Geeks\n"
        "/add_student Руслан\n"
        "/enroll 1 2\n\n"
        "<b>Удаление:</b>\n"
        "/delete_course 1\n"
        "/delete_student 1\n"
        "/unenroll 1 2\n\n"
        "Первое число — ID студента, второе — ID курса."
    )


@dp.message(F.text.startswith("/add_course"))
async def add_course(message: Message):
    title = message.text.replace("/add_course", "", 1).strip()
    if not title:
        await message.answer(
            "❌ Укажите название курса.\n\n"
            "Пример:\n<code>/add_course Geeks</code>"
        )
        return

    cursor.execute("INSERT INTO courses (title) VALUES (?)", (title,))
    conn.commit()
    course_id = cursor.lastrowid

    await send_main(
        message,
        f"✅ Курс добавлен.\n\nID: <b>{course_id}</b>\nНазвание: <b>{title}</b>"
    )


@dp.message(F.text.startswith("/add_student"))
async def add_student(message: Message):
    name = message.text.replace("/add_student", "", 1).strip()
    if not name:
        await message.answer(
            "❌ Укажите имя студента.\n\n"
            "Пример:\n<code>/add_student Эмили</code>"
        )
        return

    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    student_id = cursor.lastrowid

    await send_main(
        message,
        f"✅ Студент добавлен.\n\nID: <b>{student_id}</b>\nИмя: <b>{name}</b>"
    )


def parse_two_ids(message: Message):
    parts = message.text.split()
    if len(parts) != 3:
        return None
    try:
        return int(parts[1]), int(parts[2])
    except ValueError:
        return None


@dp.message(F.text.startswith("/enroll"))
async def enroll_student(message: Message):
    ids = parse_two_ids(message)
    if not ids:
        await message.answer(
            "❌ Неверный формат.\n\n"
            "<code>/enroll ID_студента ID_курса</code>\n\n"
            "Например: <code>/enroll 1 2</code>"
        )
        return

    student_id, course_id = ids
    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        await message.answer("❌ Студент с таким ID не найден.")
        return

    cursor.execute("SELECT title FROM courses WHERE id = ?", (course_id,))
    course = cursor.fetchone()
    if not course:
        await message.answer("❌ Курс с таким ID не найден.")
        return

    cursor.execute(
        "SELECT 1 FROM student_course WHERE student_id = ? AND course_id = ?",
        (student_id, course_id),
    )
    if cursor.fetchone():
        await message.answer("⚠️ Студент уже записан на этот курс.")
        return

    cursor.execute(
        "INSERT INTO student_course (student_id, course_id) VALUES (?, ?)",
        (student_id, course_id),
    )
    conn.commit()

    await send_main(
        message,
        f"✅ Студент <b>{student[0]}</b> записан на курс <b>{course[0]}</b>."
    )


@dp.callback_query(F.data == "courses")
async def show_courses(callback: CallbackQuery):
    cursor.execute("SELECT id, title FROM courses ORDER BY title")
    courses = cursor.fetchall()
    await callback.answer()

    if not courses:
        await callback.message.answer("📚 Курсов пока нет.", reply_markup=main_menu())
        return

    text = "<b>📚 Список курсов</b>\n\n"
    text += "".join(f"🆔 {course_id} — <b>{title}</b>\n" for course_id, title in courses)
    await callback.message.answer(text, reply_markup=main_menu())


@dp.callback_query(F.data == "course_students")
async def choose_course(callback: CallbackQuery):
    cursor.execute("SELECT id, title FROM courses ORDER BY title")
    courses = cursor.fetchall()
    await callback.answer()

    if not courses:
        await callback.message.answer("Курсов пока нет.", reply_markup=main_menu())
        return

    rows = [[(title, f"course:{course_id}")] for course_id, title in courses]
    rows.append([("⬅️ Главное меню", "main_menu")])
    await callback.message.answer("Выберите курс:", reply_markup=keyboard(*rows))


@dp.callback_query(F.data.startswith("course:"))
async def show_course_students(callback: CallbackQuery):
    course_id = int(callback.data.split(":")[1])

    cursor.execute("""
        SELECT students.name, courses.title
        FROM student_course
        JOIN students ON students.id = student_course.student_id
        JOIN courses ON courses.id = student_course.course_id
        WHERE courses.id = ?
        ORDER BY students.name
    """, (course_id,))
    students = cursor.fetchall()
    await callback.answer()

    if not students:
        await callback.message.answer(
            "На этот курс пока никто не записан.",
            reply_markup=main_menu()
        )
        return

    text = f"<b>📚 Курс: {students[0][1]}</b>\n\n"
    text += "".join(f"{i}. {name}\n" for i, (name, _) in enumerate(students, 1))
    await callback.message.answer(text, reply_markup=main_menu())


@dp.callback_query(F.data == "students")
async def show_students(callback: CallbackQuery):
    cursor.execute("""
        SELECT students.id, students.name, courses.title
        FROM students
        LEFT JOIN student_course ON students.id = student_course.student_id
        LEFT JOIN courses ON courses.id = student_course.course_id
        ORDER BY students.name
    """)
    rows = cursor.fetchall()
    await callback.answer()

    if not rows:
        await callback.message.answer("Студентов пока нет.", reply_markup=main_menu())
        return

    text = "<b>👥 Все студенты</b>\n\n"
    current_student = None

    for student_id, name, course in rows:
        if student_id != current_student:
            if current_student is not None:
                text += "\n"
            text += f"🆔 {student_id} — <b>{name}</b>\n"
            current_student = student_id
        text += f"   📚 {course}\n" if course else "   — пока без курса\n"

    await callback.message.answer(text, reply_markup=main_menu())


@dp.callback_query(F.data == "popular")
async def popular_courses(callback: CallbackQuery):
    cursor.execute("""
        SELECT courses.title, COUNT(student_course.student_id)
        FROM student_course
        JOIN courses ON courses.id = student_course.course_id
        GROUP BY courses.id
        HAVING COUNT(student_course.student_id) >= 2
        ORDER BY COUNT(student_course.student_id) DESC
    """)
    courses = cursor.fetchall()
    await callback.answer()

    if not courses:
        await callback.message.answer(
            "🔥 Пока нет курсов с двумя и более студентами.",
            reply_markup=main_menu()
        )
        return

    text = "<b>🔥 Популярные курсы</b>\n\n"
    text += "".join(f"📚 {title} — <b>{count}</b> студентов\n" for title, count in courses)
    await callback.message.answer(text, reply_markup=main_menu())


@dp.callback_query(F.data == "manage")
async def manage(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "<b>⚙️ Управление</b>\n\n"
        "Для добавления используются команды:\n\n"
        "<code>/add_course Geeks</code>\n"
        "<code>/add_student Артур</code>\n"
        "<code>/enroll 1 2</code>\n\n"
        "Выберите действие:",
        reply_markup=manage_menu()
    )


HELP_TEXT = {
    "add_course_help": "➕ <b>Добавление курса</b>\n\nНапишите:\n<code>/add_course Название курса</code>\n\nНапример:\n<code>/add_course GeekTech</code>",
    "add_student_help": "➕ <b>Добавление студента</b>\n\nНапишите:\n<code>/add_student Имя</code>\n\nНапример:\n<code>/add_student Алексей</code>",
    "enroll_help": "🔗 <b>Запись студента на курс</b>\n\nФормат:\n<code>/enroll ID_студента ID_курса</code>\n\nНапример:\n<code>/enroll 1 2</code>",
    "delete_course": "❌ <b>Удаление курса</b>\n\nНапишите:\n<code>/delete_course ID</code>\n\nНапример:\n<code>/delete_course 2</code>",
    "delete_student": "❌ <b>Удаление студента</b>\n\nНапишите:\n<code>/delete_student ID</code>\n\nНапример:\n<code>/delete_student 1</code>",
    "unenroll": "🔗 <b>Убрать студента с курса</b>\n\nФормат:\n<code>/unenroll ID_студента ID_курса</code>\n\nНапример:\n<code>/unenroll 1 2</code>",
}


@dp.callback_query(F.data.in_(HELP_TEXT.keys()))
async def help_action(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(HELP_TEXT[callback.data])


@dp.message(F.text.startswith("/delete_course"))
async def delete_course(message: Message):
    value = message.text.replace("/delete_course", "", 1).strip()
    if not value.isdigit():
        await message.answer("❌ Укажите ID курса.\n\nНапример: <code>/delete_course 2</code>")
        return

    course_id = int(value)
    cursor.execute("SELECT title FROM courses WHERE id = ?", (course_id,))
    course = cursor.fetchone()
    if not course:
        await message.answer("❌ Курс не найден.")
        return

    cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    await send_main(message, f"🗑 Курс <b>{course[0]}</b> удалён.")


@dp.message(F.text.startswith("/delete_student"))
async def delete_student(message: Message):
    value = message.text.replace("/delete_student", "", 1).strip()
    if not value.isdigit():
        await message.answer("❌ Укажите ID студента.\n\nНапример: <code>/delete_student 1</code>")
        return

    student_id = int(value)
    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        await message.answer("❌ Студент не найден.")
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    await send_main(message, f"🗑 Студент <b>{student[0]}</b> удалён.")


@dp.message(F.text.startswith("/unenroll"))
async def unenroll_student(message: Message):
    ids = parse_two_ids(message)
    if not ids:
        await message.answer("❌ Неверный формат.\n\n<code>/unenroll 1 2</code>")
        return

    student_id, course_id = ids
    cursor.execute(
        "SELECT 1 FROM student_course WHERE student_id = ? AND course_id = ?",
        (student_id, course_id),
    )
    if not cursor.fetchone():
        await message.answer("❌ Такой связи нет.")
        return

    cursor.execute(
        "DELETE FROM student_course WHERE student_id = ? AND course_id = ?",
        (student_id, course_id),
    )
    conn.commit()
    await send_main(message, "✅ Студент удалён с курса.")


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "<b>📚 Курсы</b>\n\nВыберите нужный раздел:",
        reply_markup=main_menu()
    )


async def main():
    print("Бот Курсов запущен.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        conn.close()