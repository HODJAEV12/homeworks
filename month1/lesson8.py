# from datetime import datetime
# def log_event(message):
#     current_time = datetime.now().strftime("%X-$m-%d %H:%M:%S")
#     with open("month1/data.txt", "a", encoding="utf-8") as file:
#         file.write(f"[{current_time}] {message} \n")
# while True:
#     print("\nMENU")
#     print("1. Войти")
#     print("2. Зарегистрироваться")
#     print("3. Создать заказ")
#     print("4. Выйти из аккаунта")
#     print("5. Завершить программу")
#     choice = input("\nВыберите действие: ")
#     if choice == "1":
#         log_event("Пользователь вошёл в систему")   
#     elif choice == "2":
#         log_event("Создан новый пользователь")
#     elif choice == "3":
#         log_event("Создан новый заказ")
#     elif choice == "4":
#         log_event("Пользователь вышел из аккаунта")  
#     elif choice == "5":
#         log_event("Пользователь вышел из системы")
#         break
#     else:
#         log_event(f"Неизвестная команда: {choice}")

# from datetime import datetime
# def ex_event(message):
#     current_time = datetime.now().strftime("%X-$m-%d %H:%M:%S")
#     with open("month1/lesson8/data.txt", "a", encoding="utf-8") as file:
#         file.write(f"[{current_time}] {message} \n")
# while True:
#     print("\nMENU")
#     print("1. Добавить задачу")
#     print("2. Показать задачи")
#     print("3. Выход")
#     choice = input("\nВыберите действие: ")
#     if choice == "1":
#         ex = input("Задача: ")
#         ex_event(f"Добавлена задача: {ex}")
#     elif choice == "2":
#         with open("month1/data.txt", "r", encoding="utf-8") as file:
#             text = file.read()
#             print(text)
#         ex_event("Пользователь посмотрел задачи")
#     elif choice == "3":
#         ex_event("Пользователь вышел из системы")
#         break
#     else:
#         print("Неизвестная команда")
#         ex_event(f"Неизвестная команда: {choice}")