from django.urls import path

from . import views

app_name = "deliveries"

urlpatterns = [
    path("", views.deliveries_list, name="list"),
    path("available/", views.available_deliveries, name="available"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:delivery_id>/", views.delivery_detail, name="detail"),
]
