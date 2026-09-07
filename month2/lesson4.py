from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, model, year):
        self.id = vehicle_id
        self.brand = brand
        self.model = model
        self.year = year
        self.__mileage = 0
        self.__fuel = 100

    def get_fuel(self):
        return self.__fuel

    def refuel(self, amount):
        if self.__fuel + amount > 100:
            print("Нельзя заправить больше 100%!")
        else:
            self.__fuel += amount
            print(f"Заправлено. Топливо: {self.__fuel}%")

    def drive(self, km):
        if km < 0:
            print("Не может быть отрицательный значение!")
            return
        
        fuel_needed = km * 0.5
        if self.__fuel < fuel_needed:
            print("Нет топлива для такой поездки!")
        else:
            self.__fuel -= fuel_needed
            self.__mileage += km
            print(f"Проехали {km} км. Пробег: {self.__mileage} км. Топливо: {self.__fuel}%")

    @property
    def mileage(self):
        return self.__mileage

    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def service(self):
        pass

class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, doors, body_type):
        super().__init__(vehicle_id, brand, model, year)
        self.doors = doors
        self.body_type = body_type

    def info(self):
        print(f"""[Легковая] ID: {self.id} | {self.brand} {self.model} ({self.year}) | Кузов: {self.body_type} | Пробег: {self.mileage} км""")

    def service(self):
        print(f"Обслуживание {self.brand}: Замена масла.")

class Truck(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, max_load):
        super().__init__(vehicle_id, brand, model, year)
        self.max_load = max_load

    def info(self):
        print(f"[Грузовик] ID: {self.id} | {self.brand} {self.model} ({self.year}) | Груз: {self.max_load} т | Пробег: {self.mileage} км")

    def service(self):
        print(f"Обслуживание {self.brand}: Замена масла и проверка гидравлики.")

class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, engine_volume):
        super().__init__(vehicle_id, brand, model, year)
        self.engine_volume = engine_volume

    def info(self):
        print(f"[Мотоцикл] ID: {self.id} | {self.brand} {self.model} ({self.year}) | Объем: {self.engine_volume}сс | Пробег: {self.mileage} км")

    def service(self):
        print(f"Обслуживание {self.brand}: Замена цепи.")

class Bus(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, seats):
        super().__init__(vehicle_id, brand, model, year)
        self.seats = seats

    def info(self):
        print(f"[Автобус] ID: {self.id} | {self.brand} {self.model} ({self.year}) | Мест: {self.seats} | Пробег: {self.mileage} км")

    def service(self):
        print(f"Обслуживание {self.brand}: Проверка пассажирских сидений.")

class Driver:
    def __init__(self, fio, age, exp, category):
        self.fio = fio
        self.age = age
        self.exp = exp
        self.category = category
        self.vehicle = None

    def assign_vehicle(self, vehicle):
        if self.vehicle:
            print(f"Водитель {self.fio} уже занят!")
        else:
            self.vehicle = vehicle
            print(f"Водитель {self.fio} сел за руль ID: {vehicle.id}")

    def remove_vehicle(self):
        self.vehicle = None
        print(f"Водитель {self.fio} теперь свободен.")

class Fleet:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        print("Транспорт добавлен.")

    def remove_vehicle(self, vehicle_id):
        v = self.find_vehicle(vehicle_id)
        if v:
            self.vehicles.remove(v)
            print("Транспорт удален.")
        else:
            print("Не найден.")

    def find_vehicle(self, vehicle_id):
        for v in self.vehicles:
            if v.id == vehicle_id:
                return v
        return None

    def show_all(self):
        for v in self.vehicles:
            v.info()

    def sort_by_year(self):
        self.vehicles.sort(key=lambda x: x.year)
        print("Отсортировано по году.")

    def sort_by_mileage(self):
        self.vehicles.sort(key=lambda x: x.mileage)
        print("Отсортировано по пробегу.")

fleet = Fleet()
drivers = []

fleet.add_vehicle(Car(1, "BMW", "M5", 2022, 4, "Седан"))
fleet.add_vehicle(Truck(2, "MAN", "TGX", 2019, 18))
drivers.append(Driver("Иванов И.И.", 30, 10, "B, C"))

while True:
    print("\n--- МЕНЮ ---")
    print("1. Добавить авто | 2. Удалить авто | 3. Показать все | 4. Найти авто")
    print("5. Обслужить     | 6. Заправить    | 7. Поехать      | 8. Назначить водителя")
    print("9. Водители      | 10. Сортировка  | 0. Выход")
    
    choice = input("Действие: ")

    if choice == "1":
        t = input("1-Car, 2-Truck, 3-Moto, 4-Bus: ")
        v_id = int(input("ID: "))
        brand = input("Марка: ")
        model = input("Модель: ")
        year = int(input("Год: "))
        
        if t == "1":
            fleet.add_vehicle(Car(v_id, brand, model, year, 4, "Седан"))
        elif t == "2":
            fleet.add_vehicle(Truck(v_id, brand, model, year, 20))
        elif t == "3":
            fleet.add_vehicle(Motorcycle(v_id, brand, model, year, 1000))
        elif t == "4":
            fleet.add_vehicle(Bus(v_id, brand, model, year, 50))

    elif choice == "2":
        v_id = int(input("Введите ID для удаления: "))
        fleet.remove_vehicle(v_id)

    elif choice == "3":
        fleet.show_all()

    elif choice == "4":
        v_id = int(input("Введите ID для поиска: "))
        v = fleet.find_vehicle(v_id)
        if v: v.info()
        else: print("Не найден.")

    elif choice == "5":
        v_id = int(input("ID транспорта для ТО: "))
        v = fleet.find_vehicle(v_id)
        if v: v.service()

    elif choice == "6":
        v_id = int(input("ID транспорта: "))
        v = fleet.find_vehicle(v_id)
        if v:
            amount = float(input("Сколько % залить?: "))
            v.refuel(amount)

    elif choice == "7":
        v_id = int(input("ID транспорта: "))
        v = fleet.find_vehicle(v_id)
        if v:
            km = float(input("Дистанция (км): "))
            v.drive(km)

    elif choice == "8":
        if not drivers: 
            print("Сначала добавьте водителя (пункт 9)")
            continue
        v_id = int(input("ID машины: "))
        v = fleet.find_vehicle(v_id)
        if v:
            drivers[0].assign_vehicle(v)

    elif choice == "9":
        opt = input("1-Показать, 2-Добавить: ")
        if opt == "1":
            for d in drivers:
                status = f"за рулем ID {d.vehicle.id}" if d.vehicle else "свободен"
                print(f"{d.fio} ({status})")
        elif opt == "2":
            fio = input("ФИО: ")
            drivers.append(Driver(fio, 30, 5, "B"))

    elif choice == "10":
        opt = input("1-По году, 2-По пробегу: ")
        if opt == "1": fleet.sort_by_year()
        elif opt == "2": fleet.sort_by_mileage()
        else: print("Ошибка!")

    elif choice == "0":
        print("Пока!")
        break