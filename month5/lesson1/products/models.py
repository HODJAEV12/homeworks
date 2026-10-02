from django.db import models

class Products(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена продукта")
    quantity = models.PositiveIntegerField(verbose_name="Количество продукта", default=0)
    is_available = models.BooleanField(default=True, verbose_name="Доступность продукта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"