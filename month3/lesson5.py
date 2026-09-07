import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

conn = sqlite3.connect("products.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    telegram_id INTEGER, 
    name TEXT, 
    quantity INTEGER
)
""")
conn.commit()

BOT_TOKEN = "8592541479:AAG02F7sXIxvPN58EcV8tBanibY2ZtThgZo"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class AddProduct(StatesGroup):
    name = State()
    quantity = State()

class DeleteProduct(StatesGroup): 
    id = State()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="add")],
        [InlineKeyboardButton(text="🛒 Мои товары", callback_data="products")],
        [InlineKeyboardButton(text="🗑 Удалить товар", callback_data="delete")]
    ]
)

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Выберите функцию:", reply_markup=keyboard)

@dp.callback_query(F.data == "add")
async def add_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Добавляем новый товар.\n\nНапишите название товара:")
    await state.set_state(AddProduct.name)

@dp.message(AddProduct.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь напишите количество товара (цифрой):")
    await state.set_state(AddProduct.quantity)

@dp.message(AddProduct.quantity)
async def get_quantity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите количество числом.")
        return

    data = await state.get_data()
    name = data["name"]
    quantity = int(message.text)
    telegram_id = message.from_user.id

    cur.execute(
        "INSERT INTO products (telegram_id, name, quantity) VALUES (?, ?, ?)",
        (telegram_id, name, quantity)
    )
    conn.commit()
    await state.clear()

    await message.answer(
        f"✅ Товар успешно сохранён!\n\n"
        f"📦 Название: {name}\n"
        f"🔢 Количество: {quantity}",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "products")
async def show_products(callback: CallbackQuery):
    await callback.answer()
    telegram_id = callback.from_user.id

    cur.execute("SELECT id, name, quantity FROM products WHERE telegram_id = ?", (telegram_id,))
    products = cur.fetchall()

    if not products:
        await callback.message.answer("У вас пока нет сохранённых товаров.", reply_markup=keyboard)
        return

    text = "🛒Ваш список покупок:\n\n"
    for item in products:
        item_id, name, quantity = item
        text += f"🆔 `{item_id}` | **{name}** — {quantity} шт.\n"

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@dp.callback_query(F.data == "delete")
async def delete_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ID товара, который хотите удалить:")
    await state.set_state(DeleteProduct.id)

@dp.message(DeleteProduct.id)
async def delete_finish(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("ID должен быть числом. Попробуйте ещё раз:")
        return

    product_id = int(message.text)
    telegram_id = message.from_user.id

    cur.execute("SELECT id FROM products WHERE id = ? AND telegram_id = ?", (product_id, telegram_id))
    product = cur.fetchone()

    if not product:
        await message.answer("Товар с таким ID не найден в вашем списке. Попробуйте снова.")
        return

    cur.execute("DELETE FROM products WHERE id = ? AND telegram_id = ?", (product_id, telegram_id))
    conn.commit()
    await state.clear()

    await message.answer(f"🗑 Товар с ID {product_id} успешно удалён!", reply_markup=keyboard)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        conn.close()