from django.urls import path

from . import views

urlpatterns = [
    path("", views.suppliers_list, name="suppliers"),
    path(
        "<int:supplier_id>/",
        views.supplier_detail,
        name="supplier_detail",
    ),
]
