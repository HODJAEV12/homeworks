### Задание1

class BankAccount:
    def __init__(self, balance=0.0):
        self.balance = balance

    @staticmethod
    def is_valid_amount(amount):
        return amount >= 0

    def deposit(self, amount):
        if self.is_valid_amount(amount):
            self.balance += amount

    def withdraw(self, amount):
        if self.is_valid_amount(amount) and amount <= self.balance:
            self.balance -= amount

    def __str__(self):
        return f"Баланс: {self.balance}"

    def __add__(self, other):
        return BankAccount(self.balance + other.balance)

    @classmethod
    def create_default_account(cls):
        return cls(1000)

acc1 = BankAccount.create_default_account()
acc2 = BankAccount(500)

acc2.deposit(200)
acc2.withdraw(100)     

acc3 = acc1 + acc2                         

print(acc1)
print(acc2)
print(acc3)

### Задание2

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} лет"

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age


class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def __str__(self):
        return f"Студент: {super().__str__()}, ID: {self.student_id}"

    @classmethod
    def create_freshman(cls, name, age):
        return cls(name, age, student_id="NEW-2026")


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def __str__(self):
        return f"Преподаватель: {super().__str__()}, Предмет: {self.subject}"

    @staticmethod
    def is_prof_age(age):
        return age >= 40


class Researcher:
    def __init__(self, topic="Общая наука"):
        self.topic = topic

    def research(self):
        return f"Проводит исследование на тему: '{self.topic}'"


class Assistant(Student, Researcher):
    def __init__(self, name, age, student_id, topic):
        Student.__init__(self, name, age, student_id)
        Researcher.__init__(self, topic)

    def __str__(self):
        return f"Ассистент: {self.name}, ID: {self.student_id}, Тема: {self.topic}"

for cls in Assistant.mro():
    print(cls)

teacher = Teacher("Иван Петрович", 45, "Программирование")
student1 = Student("Алексей", 20, "ST-105")
assistant = Assistant("Мария", 23, "AST-99", "Нейросети")

print(teacher)
print(student1)
print(assistant)

print(assistant.research())

print(f"Возраст {teacher.age} подходит для профессора? {Teacher.is_prof_age(teacher.age)}")

freshman = Student.create_freshman("Дмитрий", 18)
print(f"Создан первокурсник: {freshman}")

student2 = Student("Алексей", 20, "ST-200")
print(f"student1 == student2? {student1 == student2}")
print(f"student1 == teacher? {student1 == teacher}")