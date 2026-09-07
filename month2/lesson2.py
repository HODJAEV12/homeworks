class Delivery:
    def __init__(self, sender, receiver, distance):
        self.sender = sender
        self.receiver = receiver
        self.distance = distance

    def deliver(self):
        print(f"Доставка от {self.sender} к {self.receiver} ({self.distance} км)")


class CarDelivery(Delivery):
    def calculate_price(self):
        return self.distance * 15

    def estimated_time(self):
        return self.distance / 60


class AirDelivery(Delivery):
    def calculate_price(self):
        return self.distance * 50 + 500

    def estimated_time(self):
        return self.distance / 700


class DroneDelivery(Delivery):
    def calculate_price(self):
        if self.distance > 30:
            return "Ошибка: Дрон не может доставить на такое расстояние"
        return self.distance * 30

    def estimated_time(self):
        if self.distance > 30:
            return 0
        return self.distance / 40

class DeliveryManager:
    def __init__(self):
        self.deliveries = []

    def add_delivery(self, delivery):
        self.deliveries.append(delivery)

    def show_all(self):
        for i in self.deliveries:
            i.deliver()
            print(f"Цена: {i.calculate_price()} | Время: {i.estimated_time()} ч.")
            print("-" * 30)

    def total_income(self):
        total = 0
        for i in self.deliveries:
            price = i.calculate_price()
            if type(price) in (int, float):
                total += price
        return total

    def most_expensive_delivery(self):
        valid_deliveries = [i for i in self.deliveries if type(i.calculate_price()) in (int, float)]
        if not valid_deliveries:
            return None
        return max(valid_deliveries, key=lambda i: i.calculate_price())

manager = DeliveryManager()

manager.add_delivery(CarDelivery("Иван", "Алексей", 120))
manager.add_delivery(AirDelivery("Склад А", "Склад Б", 1000))
manager.add_delivery(DroneDelivery("Пицца", "Клиент", 5))
manager.add_delivery(DroneDelivery("Магазин", "Дача", 50))

print(" --- ВСЕ ДОСТАВКИ --- ")
manager.show_all()

print(f"Общий доход: {manager.total_income()}")

expensive = manager.most_expensive_delivery()
if expensive:
    print("\n --- САМАЯ ДОРОГАЯ ДОСТАВКА --- ")
    expensive.deliver()
    print(f"Цена: {expensive.calculate_price()}")