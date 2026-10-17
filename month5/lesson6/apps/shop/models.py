from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shops',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )
    name = models.CharField(max_length=60, verbose_name='Название')
    color = models.CharField(max_length=30, verbose_name='Цвет')
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name='Логотип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
