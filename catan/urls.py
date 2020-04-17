"""catan URL Configuration
"""
from django.contrib import admin
from django.urls import path

from pieces import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', views.show_board, name='show-board'),
]
