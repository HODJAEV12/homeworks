# 1

# tovar = ["телефон", "планшет", "наушники", "телевизор"]
# print(len(tovar))
# print(tovar.append("клавиатура"))
# print(tovar[0])
# print(tovar[-1])

# 2

# numbers = [1, 2, 3, 4, 5]
# print(f"Сумма всех чисел: {sum(numbers)}")
# print(f"Максимальное число: {max(numbers)}")
# print(f"Минамальное число: {min(numbers)}")
# count = 0
# for i in numbers:
#     if i % 2 == 0:
#         count += 1
# print(f"Количетсво четных чисел: {count}")
# print(numbers.append(100))

# 3

# students = ("Beka", "Nurik", "Islam", "Aziz", "Mahmud")
# print(f"Количество студнетов: {len(students)}")
# print("Индекс Ислама:", students.index("Islam"))
# for i in students:
#     if i == "Beka":
#         print("В кортеже есть Бека")
#     print(i)

# 4

# cities = ("Osh", "Madrid", "Batken", "Osh", "Talas")
# print(cities[0])
# print(cities[-1])
# count = 0
# for i in set(cities):
#     if cities.count(i) > 1:
#         print(f"Количетсво одинаковых городов: {cities.count(i)}")
#     if i == "Madrid":
#         print("В кортеже есть Madrid")
#     print(i)
# print(f"Количество одинаковых городов: {count}")

# 5

# mark = [2, 4, 4, 5, 3, 2, 4, 5, 3, 2, 4, 5, 3, 3]
# mark = tuple(mark)
# print(f"Средняя оценка: {sum(mark) / len(mark)}")
# count = 0
# for i in mark:
#     if i == 5:
#         count += 1
# print(f"Количество хороших оценок: {count}")
# print(f"Минимальная оценка: {min(mark)}")
# print(f"Максимальная оценка: {max(mark)}")