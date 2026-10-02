from django.db import models

class Books(models.Model):
    author = models.CharField(max_length=40, verbose_name="Автор книги")
    title = models.CharField(max_length=70, verbose_name="Название книги")
    description = models.TextField(verbose_name="Описание книги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена книги")
    year = models.DateField(verbose_name="Год выпуска книги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"