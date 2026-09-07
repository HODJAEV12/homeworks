### Задание1

# from abc import ABC, abstractmethod

# class Animal(ABC):
#     @abstractmethod
#     def make_sound(self):
#         pass

# class Dog(Animal):
#     def make_sound(self):
#         print(f"Гав!")
    
# class Cat(Animal):
#     def make_sound(self):
#         print(f"Мяу!")

# class Bird(Animal):
#     def make_sound(self):
#         print(f"Ку-ку!")

# dog = Dog()
# cat = Cat()
# bird = Bird()

# dog.make_sound()
# cat.make_sound()
# bird.make_sound()

### Задание2

# class BankAccount:
#     def __init__(self, owner, balance=0):
#         self.owner = owner
#         self.__balance = balance

#     def deposit(self, amount):
#         if amount < 0:
#             print("Ошибка! Нельзя пополнить счет на отрицательную сумму")
#         else:
#             self.__balance = self.__balance + amount
#             print(f"Счет пополнен на {amount}. Новый баланс: {self.__balance}")

#     def withdraw(self, amount):
#         if amount > self.__balance:
#             print("Ошибка! Недостаточно денег на счету")
#         else:
#             self.__balance = self.__balance - amount
#             print(f"Снято {amount}. Остаток: {self.__balance}")

#     def get_balance(self):
#         return self.__balance

#     def calculate_profit(self):
#         return 0 

# class CreditAccount(BankAccount):
#     def __init__(self, owner, balance=0, credit_limit=1000):
#         super().__init__(owner, balance)
#         self.credit_limit = credit_limit

#     def calculate_profit(self):
#         current_balance = self.get_balance()
#         if current_balance < 0:
#             return current_balance * 0.1
#         else:
#             return 0


# class SavingsAccount(BankAccount):
#     def __init__(self, owner, balance=0, percent=5):
#         super().__init__(owner, balance)
#         self.percent = percent

#     def calculate_profit(self):
#         current_balance = self.get_balance()
#         profit = current_balance * (self.percent / 100)
#         return profit

# print("--- Проверка Ивана (Обычный счет) ---")
# ivan_account = BankAccount("Иван", 500)
# ivan_account.deposit(-100)
# ivan_account.withdraw(600)
# ivan_account.deposit(200)

# print("\n--- Проверка Марии (Накопительный счет) ---")
# maria_account = SavingsAccount("Мария", 1000, percent=10)
# print("Баланс Марии:", maria_account.get_balance())
# print("Прибыль Марии по процентам:", maria_account.calculate_profit())

# print("\n--- Проверка Петра (Кредитный счет) ---")
# petya_account = CreditAccount("Петр", 0, credit_limit=500)
# print("Прибыль Петра:", petya_account.calculate_profit())

### Задание3

from abc import ABC, abstractmethod

class Delivery(ABC):
    def __init__(self, address, price):
        self.address = address
        self.price = price

    @abstractmethod
    def deliver(self):
        pass

    def calculate_price(self):
        return self.price

class CourierDelivery(Delivery):
    def __init__(self, address, price, courier_name):
        super().__init__(address, price)
        self.courier_name = courier_name

    def deliver(self):
        print(f"Курьер {self.courier_name} пешком несёт заказ по адресу: {self.address}")

class CarDelivery(Delivery):
    def __init__(self, address, price_per_km, distance):
        super().__init__(address, 0)
        self.price_per_km = price_per_km
        self.distance = distance
        self.price = self.calculate_price()

    def calculate_price(self):
        return self.distance * self.price_per_km

    def deliver(self):
        print(f"Машина везет заказ по адресу: {self.address}. Расстояние: {self.distance} км.")


# Доставка дроном
class DroneDelivery(Delivery):
    def __init__(self, address, price, max_weight):
        super().__init__(address, price)
        self.max_weight = max_weight

    def check_weight(self, current_weight):
        if current_weight > self.max_weight:
            print("Внимание! Заказ слишком тяжелый для дрона!")
            return False
        else:
            print("Вес в норме. Дрон готов к вылету.")
            return True
    
    def deliver(self):
        print(f"Дрон летит по воздуху на адрес: {self.address}.")

class Order:
    def __init__(self, delivery_type):
        self.products = []
        self.__total_price = 0
        self.delivery_type = delivery_type

    def add_product(self, product_name, product_price):
        self.products.append(product_name)
        self.__total_price = self.__total_price + product_price
        print(f"Добавлен товар: {product_name} ({product_price}).")

    def remove_product(self, product_name, product_price):
        if product_name in self.products:
            self.products.remove(product_name)
            self.__total_price = self.__total_price - product_price
            print(f"Удален товар: {product_name}")
        else:
            print("Такого товара нет в заказе.")

    def get_total_price(self):
        delivery_price = self.delivery_type.calculate_price()
        total_price = self.__total_price + delivery_price
        return total_price

delivery1 = CourierDelivery(address="ул. Ленина 10", price=150, courier_name="Иван")
delivery2 = CarDelivery(address="ул. Загородная 50", price_per_km=40, distance=15)
delivery3 = DroneDelivery(address="пр. Мира 25", price=500, max_weight=5)

deliveries = [delivery1, delivery2, delivery3]

for delivery in deliveries:
    delivery.deliver()
    print(f"Стоимость этой доставки: {delivery.calculate_price()}")
    print("-" * 30)

my_order = Order(delivery_type=delivery2)

my_order.add_product("Пицца", 600)
my_order.add_product("Кола", 100)

print("\nПроверка веса для дрона:")
delivery3.check_weight(current_weight=7)

print(f"\nИтоговая стоимость всего заказа: {my_order.get_total_price()}")