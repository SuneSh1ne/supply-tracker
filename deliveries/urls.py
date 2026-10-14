from django.urls import path

from . import views

app_name = "deliveries"

urlpatterns = [
    path("", views.deliveries_list, name="list"),
    path("<int:delivery_id>/", views.delivery_detail, name="detail"),
]
