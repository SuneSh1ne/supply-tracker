"""Django-модель поставки."""
from django.db import models

from products.models import Product
from suppliers.models import Supplier


class Delivery(models.Model):
    """Поставка товара от поставщика."""

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="deliveries",
        verbose_name="Поставщик",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="deliveries",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    delivery_date = models.DateField(verbose_name="Дата поставки")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    is_cancelled = models.BooleanField(default=False, verbose_name="Отменена")

    class Meta:
        ordering = ["delivery_date", "id"]
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"

    def calculate_total_cost(self):
        """Рассчитать итоговую стоимость поставки."""
        return self.quantity * self.product.price

    def cancel(self):
        """Отменить поставку."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        return (
            f"Поставка #{self.pk}: {self.product} "
            f"от {self.supplier} ({self.delivery_date})"
        )
