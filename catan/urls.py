"""catan URL Configuration
"""
from django.contrib import admin
from django.urls import path

from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', views.show_board, name='show-board'),
]
