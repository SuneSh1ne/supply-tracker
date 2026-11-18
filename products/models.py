"""Django-модель товара."""
from django.db import models
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


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
        help_text="Укажите цену за единицу товара в рублях.",
    )
    is_expensive = models.GeneratedField(
        expression=Case(
            When(price__gte=1000, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Дорогой товар",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name)) or "product"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL подробной страницы товара."""
        return reverse("products:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
