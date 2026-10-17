from django.db import models

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Zone(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name='название локации')
    location = models.CharField(max_length=255, verbose_name='город/район')
    coordinates = models.CharField(max_length=255, verbose_name='координаты')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'зона'
        verbose_name_plural = 'зоны'

    def __str__(self):
        return self.name

class Visitors(AbstractBaseModel):
    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        related_name='visitors',
        verbose_name='зона'
    )
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    info = models.TextField(verbose_name='информация о посетителе')
    is_allowed = models.BooleanField(default=False, verbose_name='разрешен ли вход')

    class Meta:
        verbose_name = 'посетитель зоны'
        verbose_name_plural = 'посетители зоны'

    def __str__(self):
        return self.full_name