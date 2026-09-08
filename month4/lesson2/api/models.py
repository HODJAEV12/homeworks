from django.db import models

class Cars(models.Model):
    brand = models.CharField(max_length=130, verbose_name="Бренд")
    color = models.CharField(max_length=100, verbose_name="Цвет")
    mileage = models.IntegerField(verbose_name="Пробег(км)")
    transmission_type = models.CharField(max_length=80, verbose_name="Тип передачи")
    fuel_type = models.CharField(max_length=100, verbose_name="Тип топлива")
    car_type = models.CharField(max_length=120, verbose_name="Тип машины(легковая, грузовая)")
    car_description = models.TextField(blank=True, verbose_name="Описание машины", default="Без описания")
    state = models.TextField(blank=True, verbose_name="Состояние", default="Не указано")
    year = models.DateField(blank=True, null=True, verbose_name="Год выхода")
    price = models.IntegerField(verbose_name="Цена(в долларах)")
    image = models.ImageField(upload_to="car_image/", verbose_name="Изображение машины", null=True, blank=True)

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
