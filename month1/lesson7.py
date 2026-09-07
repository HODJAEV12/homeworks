## Функции -- DEF

# def numbers():
#     num1 = int(input("Введите первое число: "))
#     num2 = int(input("Введите второе число: "))
#     print(num1 + num2)
# numbers()

# def info(name, age):
#     print(f"Имя: {name}, возраст: {age}")
# info("Geeks", 9)
# info("Osh", 30)

# def result(number):
#     if number % 2 == 0:
#         print(f"Число {number} чётное")
#     else:
#         print(f"Число {number} не чётное")
# result(108)

## Анонимные функции -- LAMBDA

# numbers = range(1 , 11)
# result_lamba = list(map(lambda i : i ** 3, numbers))
# print(result_lamba)

# result = lambda num1, num2: num1 + num2
# print(result(45, 12))

# numbers = range(1, 11)
# result = list(filter(lambda num : num % 2 == 0, numbers))
# print(result)