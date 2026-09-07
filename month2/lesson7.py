##### Реляционные базы данных и типы соотношения таблиц. Агрегационные функции и группировка данных. Вложенные запросы. Views

### Реляционные базы данных - базы данных, которые хранят данные в виду - ключ : значение, как словари

### Типы соотношения таблиц

# One To One (1:1)
# Одному пользователю соответствует один паспорт

# One To Many (1:N) Самый популярный вид
# Один пользователь может сделать много заказов

# Many To Many (M:N): Студенты <-> Курсы
# Один студент может проходить много курсов
# Один курс проходят много студентов

### Агрегационные функции - вспомогательные функции(уже встроенные)

# INNER JOIN
# INNER JOIN — это команда в SQL для соединения двух таблиц. 
# Она возвращает только те строки, которые имеют одинаковые значения в обеих таблицах
# Покажем пользователей вместе с их заказами

# LEFT JOIN
# LEFT JOIN — это команда в SQL для соединения двух таблиц, 
# которая сохраняет все строки из левой таблицы и добавляет к ним совпадения из правой
# Добавим пользователя без заказов

# Еще sum, count, max, min, avg, ...

### Вложенные запросы - запрос внутри запроса

# --------------------------------------------------------------

import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# cursor.execute("""
#     create table if not exists users(
#     id integer primary key autoincrement,
#     name text,
#     age integer
#     )
# """)

# cursor.execute("""
#     create table if not exists orders(
#         id integer primary key,
#         user_id integer,
#         product text,
#         price integer,
#         foreign key(user_id) references users(id)
#     )
# """)

# users = [ ("Bob", 20) ,("Alice", 21), ("John", 22) ]
# cursor.executemany("insert into users(name, age) values(?, ?)", users)

# products = [ 
#     (1, "iPhone", 1000), 
#     (1, "AirPods", 200),
#     (2, "Laptop", 1500),
#     (2, "Mouse", 50),
#     (3, "Keyboard", 120)
# ]
# cursor.executemany("insert into orders(user_id, product, price) values(?, ?, ?)", products)

### Агрегационные функции

## Inner join

# cursor.execute("""
#     select users.name, orders.product, orders.price
#     from users inner join orders on users.id = orders.id
# """)
# for row in cursor.fetchall():print(row)

# cursor.execute("insert into users(name, age) values('Sara', 25)")

## Left join

# cursor.execute("""
#     select users.name, orders.product
#     from users left join orders on users.id = orders.user_id
# """)
# for row in cursor.fetchall():print(row)

# Count, sum, avd, max, min

# cursor.execute("select count(*) from orders")
# print("Count:", cursor.fetchall()[0][0])

# cursor.execute("select sum(price) from orders")
# print("Sum:", cursor.fetchall()[0][0])

# cursor.execute("select avg(price) from orders")
# print("Avg:", cursor.fetchall()[0][0])

# cursor.execute("select max(price) from orders")
# print("Max:", cursor.fetchall()[0][0])

# cursor.execute("select min(price) from orders")
# print("Min:", cursor.fetchall()[0][0])

### Группировка данных

# cursor.execute("""
#     select users.name, sum(orders.price)
#     from users join orders
#     on users.id = orders.user_id
#     group by users.name
# """)
# for row in cursor.fetchall(): print(row)

### Вложенные запросы

# cursor.execute("""
#     select name from users where id = (
#         select user_id from orders where price = (
#             select max(price) from orders
#         )
#     )
# """)
# print(cursor.fetchone()[0])

### Views

conn.commit()
conn.close()