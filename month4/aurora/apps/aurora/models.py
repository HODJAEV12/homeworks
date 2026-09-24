from django.db import models

class Settings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="Имя сайта")
    short_description = models.CharField(max_length=300, verbose_name="Краткое описание")
    locate = models.CharField(max_length=250, verbose_name="Локация")
    phone = models.CharField(max_length=250, verbose_name="Телефонный номер")
    email = models.CharField(max_length=250, verbose_name="Электронная почта")
    reception = models.CharField(max_length=250, verbose_name="О ресепшене")

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Основная настройка"
        verbose_name_plural = "Основные настройки"

class Banner(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    sub_title = models.CharField(max_length=250, verbose_name="Подзаголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="banner/", verbose_name="Фото")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class Advantages(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    sub_title = models.CharField(max_length=250, verbose_name="Подзаголовок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Преимущетсво"
        verbose_name_plural = "Преимущетсва"

class About_hotel(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    sub_title = models.CharField(max_length=250, verbose_name="Подзаголовок")
    rooms_count = models.IntegerField(verbose_name="Количество номеров")
    rating = models.FloatField(verbose_name="Рейтинг гостей(до 10)")
    works_age = models.IntegerField(verbose_name="Лет работы")
    image = models.ImageField(upload_to="about/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Характеристика отеля"
        verbose_name_plural = "Характеристики отеля"

class Rooms(models.Model):
    image = models.ImageField(upload_to="rooms/", verbose_name="Фото номера")
    room_class = models.CharField(verbose_name="Класс")
    description = models.TextField(verbose_name="Описание комнаты")
    guests_count = models.IntegerField(verbose_name="Количество гостей")
    square = models.IntegerField(verbose_name="Площадь")
    advantage = models.CharField(max_length=250, verbose_name="Преимущество")
    price = models.IntegerField(verbose_name="Цена(ночь)")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"