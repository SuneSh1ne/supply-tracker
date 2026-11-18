"""Административный интерфейс поставок."""
from django.contrib import admin, messages

from deliveries.models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "supplier",
        "product",
        "product_price",
        "quantity",
        "delivery_date",
        "is_paid",
        "status",
    )
    list_display_links = ("id",)
    search_fields = ("supplier__name", "product__name")
    list_filter = ("delivery_date", "status", "is_paid")
    ordering = ("-delivery_date",)
    list_per_page = 20
    list_select_related = ("supplier", "product")
    readonly_fields = ("id",)
    date_hierarchy = "delivery_date"
    autocomplete_fields = ("supplier", "product")
    actions = ("cancel_deliveries", "restore_deliveries")

    @admin.display(description="Цена товара", ordering="product__price")
    def product_price(self, obj):
        return obj.product.price

    @admin.action(description="Отменить выбранные поставки")
    def cancel_deliveries(self, request, queryset):
        count = 0
        for delivery in queryset:
            delivery.cancel()
            count += 1
        self.message_user(
            request,
            f"Отменено поставок: {count}.",
            messages.SUCCESS,
        )

    @admin.action(description="Вернуть в активные")
    def restore_deliveries(self, request, queryset):
        updated = queryset.update(status=Delivery.Status.ACTIVE)
        self.message_user(
            request,
            f"Возвращено поставок: {updated}.",
            messages.SUCCESS,
        )
