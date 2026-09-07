##### Базы данных и СУБД. Работа с БД в Python. Основы SQL, создание таблиц и типы данных, CRUD операции

# СУБД (Система управления базами данных) — это программа, которая позволяет создавать, изменять и читать базы данных

# Реляционные базы данных хранят информацию в виде 
# связанных таблиц (строк и столбцов) со строгой схемой, используя язык SQL. 
# Они идеальны для сложных транзакций, требующих высокой надежности. 
# Нереляционные (NoSQL) базы данных используют гибкие форматы (документы JSON, ключ-значение, графы) 
# и отлично подходят для быстрого масштабирования и неструктурированных данных

## CRUD операции(CREATE, READ, UPDATE, DELETE)
# Создать таблицу - CREATE TABLE
# Добавить данные - INSERT
# Получить данные - SELECT
# Изменять - UPDATE
# Удалить - DELETE


## Типы данных
# INTEGER - целое число
# TEXT - строка
# ...

### Создание базы данных

import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

## Создание таблицы

# cursor.execute(
#     """
#     create table if not exists users(
#         id integer primary key autoincrement,
#         name text,
#         age integer
#     )
# """)
# cursor.execute(
#     """
#         insert into users(name, age)
#         values(?, ?)
#     """, ("Bob", 20)
# )

# users = [
#     ("Alice", 20),
#     ("Tom", 22),
#     ("Jack", 21)
# ]
# cursor.executemany(
#     "insert into users(name, age) values(?, ?)",
#     users
# )

## Получение данных

# Получение всей таблицы

# cursor.execute("select * from users")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# Получение определенной строки таблицы

# cursor.execute("select * from users where id = 3")
# user = cursor.fetchone()
# print(user)

### Изменение данных

# cursor.execute("""
#   
# """
# )

### Удаление данных

# cursor.execute("delete from users where id = ?", (1, ))


conn.commit() # Сохранить все изменения
conn.close() # Закрывается соединение