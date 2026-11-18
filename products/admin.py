"""Административный интерфейс товаров."""
from django.contrib import admin

from deliveries.models import Delivery
from products.models import Product


class DeliveryInline(admin.TabularInline):
    """Поставки, связанные с товаром."""

    model = Delivery
    fields = ("supplier", "quantity", "delivery_date", "is_paid", "status")
    extra = 0
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    list_display_links = ("name",)
    list_editable = ("price",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (DeliveryInline,)
    view_on_site = True
