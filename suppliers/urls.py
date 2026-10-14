from django.urls import path

from . import views

app_name = "suppliers"

urlpatterns = [
    path("", views.suppliers_list, name="list"),
    path("<int:supplier_id>/", views.supplier_detail, name="detail"),
]
