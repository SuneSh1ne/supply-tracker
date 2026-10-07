from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("deliveries/", include("deliveries.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("products/", include("products.urls")),
]
