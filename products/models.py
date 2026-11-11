"""Django-модель товара."""
from django.db import models


class Product(models.Model):
    """Товар с фиксированной ценой."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
