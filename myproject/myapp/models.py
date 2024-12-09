from django.db import models

# Create your models here.
from django.db import models

class SalesRecord(models.Model):
    date = models.DateField(verbose_name="Дата")
    product = models.CharField(max_length=100, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        unique_together = ('date', 'product')  # Проверка на дубликаты по дате и продукту

    def __str__(self):
        return f"{self.product} ({self.date})"
