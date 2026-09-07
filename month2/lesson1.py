# ---------------- Классы ----------------

# class Cat:
#     def __init__(self, name, age, sound):
#         self.name = name
#         self.age = age
#         self.sound = sound

#     def info(self):
#         print(f"{self.name} ему {self.age} года, он издаёт звук {self.sound}!")

# cat1 = Cat("Bob", 3, "мяу")
# cat1.info()

# class Students:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
    
#     def info(self):
#         print(f"Имя студента {self.name}")
#         print(f"Возраст студента {self.age}")

# student1 = Students("Alice", 20)
# student2 = Students("Bob", 22)
# student3 = Students("Abdulloh", 14)

# student1.info()
# student2.info()
# student3.info()

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.amount = amount
        print(f"Депозит успешно выполнен! {amount}")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print("Недостаточно средств на счёте!")
        else:
            self.balance -= amount
            print(f"Снятие успешно выполнено! {amount}")

    def show_balance(self):
        print(f"Баланс: {self.balance}")

account = BankAccount("Alice", 1000)
account.show_balance()
account.deposit(500)
account.withdraw(300)
account.show_balance()