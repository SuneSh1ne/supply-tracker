"""Главная страница приложения."""
from django.shortcuts import render


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")
