"""Административный интерфейс поставщиков."""
from django.contrib import admin
from django.db.models import Count, Q

from deliveries.models import Delivery
from suppliers.models import Supplier


class DeliveryInline(admin.TabularInline):
    """Поставки, связанные с поставщиком."""

    model = Delivery
    fields = ("product", "quantity", "delivery_date", "is_paid", "status")
    extra = 0
    can_delete = False


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active_deliveries_count")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (DeliveryInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            active_deliveries=Count(
                "deliveries",
                filter=Q(deliveries__status="active"),
            ),
        )

    @admin.display(description="Активных поставок", ordering="active_deliveries")
    def active_deliveries_count(self, obj):
        return obj.active_deliveries
