from django.db import models


class Stocks(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название продукта')
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
