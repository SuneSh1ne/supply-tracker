from django.urls import path

from . import views

urlpatterns = [
    path("", views.deliveries_list, name="deliveries"),
    path(
        "<int:delivery_id>/",
        views.delivery_detail,
        name="delivery_detail",
    ),
]
