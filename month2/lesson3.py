# ------------- Принципы ООП - Абстракция, Инкапсуляция -------------

### Инкапсуляция

# class BankAccount:
#     def __init__(self):
#         self.__balance = 1000
    
#     def get_balance(self):
#         return self.__balance
    
#     def deposit(self, amount):
#         self.__balance += amount

# account = BankAccount()

# account.deposit(500)

# print(account.get_balance())

# class User:
#     def __init__(self):
#         self.__age = 18
    
#     @property
#     def age(self):
#         return self.__age

#     @age.setter
#     def age(self, value):
#         if value >= 0:
#             self.__age = value

# user = User()
# user.age = 25
# print(user.age)

    # 3 вида инкапсуляции
    # публичный - self.name
    # защищённый - self._name
    # приватный - self.__name

### Абстракция

# from abc import ABC, abstractmethod

# class Animal(ABC):
#     @abstractmethod
#     def sound(self):
#         pass

# class Dog(Animal):
#     def sound(self):
#         print("Гав")

# class Cat(Animal):
#     def sound(self):
#         print("Мяу")

# dog = Dog()
# dog.sound()

# cat = Cat()
# cat.sound()

### Практика

from abc import ABC, abstractmethod

persons = []

class Employee(ABC):
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary
    
    @abstractmethod
    def work(self):
        pass

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value >= 0:
            self.__salary = value
    
class Programmer(Employee):
    def work(self):
        if self.salary < 0:
            print("Зарплата не может быть отрицательной!")
            return
        print(f"Имя сотрудника: {self.name}")
        print(f"Зарплата сотрудника: {self.salary}")
        persons.append(self.name)

class Designer(Employee):
    def work(self):
        if self.salary < 0:
            print("Зарплата не может быть отрицательной!")
            return
        print(f"Имя сотрудника: {self.name}")
        print(f"Зарплата сотрудника: {self.salary}")
        persons.append(self.name)

class Manager(Employee):
    def work(self):
        if self.salary < 0:
            print(f"Зарплата не может быть отрицательной!")
            return
        print(f"Имя сотрудника: {self.name}")
        print(f"Зарплата сотрудника: {self.salary}")
        persons.append(self.name)

programmer = Programmer("Maksim", 70000)
programmer.work()
programmer.salary = 75000
print(f"Изменённая зарплата: {programmer.salary}")

designer = Designer("Vlad", 40000)
designer.work()
designer.salary = 30000
print(f"Изменённая зарплата: {designer.salary}")

manager = Manager("Mark", 55000)
manager.work()
manager.salary = 60000
print(f"Изменённая зарплата: {manager.salary}")

manager = Manager("Vova", -5000)
manager.work()

print(f"Список сотрудников: {persons}")