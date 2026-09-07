###### ООП - Магические, классовые и статичные методы

## Магические методы

# init - создание объекта
# str - красивый вывод
# repr - представление объекта
# len - len()
# add - +
# sub - -
# mul - *
# eq - ==
# lt - <
# gt - >

# class User:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.music = []

#     def __str__(self):
#         return f"User(name = {self.name}, age = {self.age})"
    
#     def add(self, song):
#         self.music.add(song)
    
#     def __len__(self):
#         return len(self.music)
    
#     def __add__(self, other):
#         if isinstance(other, User):
#             return User(self.name + " & " + other.name, self.age + other.age)
#         return NotImplemented
    
#     def __eq__(self, other):
#         if isinstance(other, User):
#             return self.name == other.name and self.age == other.age
#         return NotImplemented

# user = User("Bob", 30)
# print(user)

# user1 = User("Alice", 25)
# user.add("Song 1")
# user.add("Song 2")
# print(len(user))

## Статичные методы

# class Nath:

#     @staticmethod
#     def add(a, b):
#         return a + b

# print(Nath.add(1, 4))

## Классовые методы

# class User:

#     users = 0

#     def __init__(self, name):
#         self.name = name
#         User.users += 1
    
#     @classmethod
#     def total_user(cls):
#         return cls.users

# User("Alice")
# User("Bob")

# print(User.total_user())

###### Множественное наследование

# class Fly:
#     def fly(self):
#         print("Летает")
    
# class Swim:
#     def swim(self):
#         print("Плавает")

# class Duck(Fly, Swim):
#     pass

# duck = Duck()

# duck.fly()
# duck.swim()

# class A:
#     def hello(self):
#         print("A")

# class B(A):
#     def hello(self):
#         print("B")

# class C(A):
#     def hello(self):
#         print("C")

# class D(B, C):
#     pass

# class E(A):
#     pass

# e = E()
# e.hello()

# d = D()
# d.hello()
# print(D.mro())

## Задание

class Camera:
    def take_photo(self): 
        print("Фотографирует")

class Phone:
    def call(self, number): 
        print(f"Звонит на номер {number}")

class SmartPhone(Camera, Phone): 
    pass

smartphone = SmartPhone()
smartphone.take_photo()
smartphone.call("+996550909800")