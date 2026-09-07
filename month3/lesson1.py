### Задание1(Лёгкое)

# class Book:
#     def __init__(self, title, author, pages):
#         self.title = title
#         self.author = author
#         self.pages = pages
    
#     def info(self):
#         print(f"Заголовок: {self.title}")
#         print(f"Автор: {self.author}")
#         print(f"Количество страниц: {self.pages}")
    
#     def read(self):
#         print(f"Читаем книгу: {self.title}")

# book = Book("Гарри Поттер", "Джоан Роулинг", 500)

# book.info()
# book.read()

### Задание2(Среднее)

# class Player:
#     def __init__(self, name, health=100, level=1):
#         self.name = name
#         self.health = health
#         self.level = level

#     def show_info(self):
#         print("Информация о игроке -->")
#         print(f"Имя игрока: {self.name}")
#         print(f"Здоровье игрока: {self.health}")
#         print(f"Уровень игрока: {self.level}")
#         print("----------------------------------")
    
#     def take_damage(self, damage):
#         self.health -= damage
#         print(f"Нанесено: {damage}. Здоровье: {self.health}")
#         if self.health <= 0:
#             print("Игрок погиб!")
#         print("----------------------------------")

#     def heal(self, amount):
#         if self.health <= 0:
#             print(f"Нельзя вылечить погибшего игрока!")
#             print("----------------------------------")
#             return
#         self.health += amount
#         print(f"Вылечено: {amount}. Здоровье: {self.health}")
#         print("----------------------------------")

#     def level_up(self):
#         self.level += 1
#         print(f"Уровень поднялся. {self.level} уровень!")
#         print("----------------------------------")

# player = Player("Knight")

# player.show_info()

# player.take_damage(30)
# player.heal(20)

# player.level_up()

# player.show_info()

### Задание3(Сложное)

# class OnlineStore:
#     def __init__(self, name):
#         self.name = name
#         self.products = []
    
#     def add_product(self, product_name):
#         self.products.append(product_name)
#         print(f"Добавлен товар: {product_name}")
    
#     def show_products(self):
#         print(f"Список товаров: {self.products}")
    
#     def count_products(self):
#         print(f"Количество товаров: {len(self.products)}")
    
#     def remove_product(self, product_name):
#         try:
#             self.products.remove(product_name)
#         except ValueError:
#             print(f"Не удалось удалить '{product_name}'! Такого товара нет!")
#             return
#         print(f"Из списка товаров идалён '{product_name}' ")

# store = OnlineStore("Tech Store")

# store.add_product("Ноутбук")
# store.add_product("Мышка")
# store.add_product("Клавиатура")

# store.show_products()
# store.count_products()

# store.remove_product("Мышка")
# store.remove_product("Наушники")

# store.show_products()