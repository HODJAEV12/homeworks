# ------------- Принципы ООП - Наследование, Полиморфизм -------------

### Наследование

# class Animal:
#     def __init__(self, name):
#         self.name = name

#     def eat(self):
#         print(f"{self.name} ест")

# class Cat(Animal): 
#     def __init__(self, name, color):
#         super().__init__(name)
#         self.color = color

#     def meow(self):
#         print(f"{self.name} мяукает")

# class Dog(Animal):
#     def __init__(self, name, age, weight):
#         super().__init__(name)
#         self.age = age
#         self.weight = weight

#     def bark(self):
#         print(f"{self.name} гавкает")

# cat = Cat("Барсик", "Серый")
# dog = Dog("Шарик", 3, 15)

# cat.eat()
# cat.meow()
# print(cat.color)

# dog.eat()
# dog.bark()
# print(f"Имя: {dog.name}. Возраст: {dog.age}. Вес: {dog.weight}")

### Полиморфизм

# class Animal:
#     def sound(self): pass

# class Cat(Animal):
#     def sound(self):
#         print("Мяу")
    
# class Dog(Animal):
#     def sound(self):
#         print("Гав")

# cat = Cat()
# cat.sound()

# dog = Dog()
# dog.sound()

### Практическая работа

class Payment: 
    def pay(self): 
        pass

products = []

class Card(Payment):
    def __init__(self, product):
        super().__init__()
        self.product = product
    
    def pay(self):
        products.append(self.product)
        print(f"Оплата картой. Товар: {self.product}")

class Cash(Payment):
    def __init__(self, product):
        super().__init__()
        self.product = product
    
    def pay(self):
        products.append(self.product)
        print(f"Оплата наличными. Товар: {self.product}")

class PayPal(Payment):
    def __init__(self, product):
        super().__init__()
        self.product = product
    
    def pay(self):
        products.append(self.product)
        print(f"Оплата переводом. Товар: {self.product}")

card = Card("Телефон")
cash = Cash("Ноутбук")
paypal = PayPal("Наушники")

card.pay()
cash.pay()
paypal.pay()

count = 0
print("Список товаров:")
for i in products:
    count += 1
    print(f"{count}. {i}")