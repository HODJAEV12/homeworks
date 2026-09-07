import sqlite3

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# cursor.execute("""
# create table if not exists orders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     product TEXT,
#     price INTEGER
# )
# """)

# orders = [
#     (1, 'iPhone', 1000),
#     (1, 'AirPods', 200),
#     (2, 'Laptop', 1500),
#     (2, 'Mouse', 50),
#     (3, 'Keyboard', 120)
# ]

# cursor.executemany("insert into orders (user_id, product, price) values (?, ?, ?)", orders)

cursor.execute("""
create view if not exists expensive_orders as
select * from orders where price > 500
""")

# cursor.execute("""
# insert into orders(user_id, product, price)
# values (3, 'MacBook', 2500)
# """)

cursor.execute("select * from expensive_orders")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("drop view if exists expensive_orders")

try:
    cursor.execute("select * from expensive_orders")
    results = cursor.fetchall()
except sqlite3.OperationalError as e:
    print(f"Ошибка! Сообщение БД: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")

conn.commit()
conn.close()