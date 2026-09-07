import sqlite3
import datetime

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

##### Создание таблицы

# cursor.execute(
# """
# create table if not exists hospital(
#     id integer primary key autoincrement,
#     name text,
#     age integer,
#     address integer,
#     phone text,
#     date text
# )
# """)

##### CRUD система

### Добавление

# date = datetime.datetime.now()

# persons = [
#     ("Abdulloh", 14, "Donskaya street", "+996550909800", date),
#     ("Muhammad", 20, "Ahmedova street", "+996554323216", date),
#     ("Abubakr", 32, "Kulatova street", "+996551299292", date),
#     ("Alice", 25, "Timurova street", "+996555959567", date)
# ]

# cursor.executemany("""insert into hospital(name, age, address, phone, date) values(?, ?, ?, ?, ?)""", persons)

### Получение данных

# Получение всех объектов

# cursor.execute("select * from hospital")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# Получение определённого объекта

# cursor.execute("select * from hospital where id = 2")
# person = cursor.fetchone()
# print(person)

### Изменение данных

# cursor.execute("update hospital set name = 'Kirill', age = 19 where id = 1")
# cursor.execute("update hospital set phone = '+996775554535', address = 'Severnaya street' where id = 2")

### Удаление объекта

# cursor.execute("delete from hospital where id = ?", (4, ))

conn.commit()
conn.close()