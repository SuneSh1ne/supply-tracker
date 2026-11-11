"""Django-модель поставщика."""
from django.db import models


class Supplier(models.Model):
    """Поставщик товаров."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name
