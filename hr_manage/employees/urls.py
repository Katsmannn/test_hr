from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('positions/', views.positions, name='positions'),
    path('positions/new/', views.new_position, name='new_position'),
    path('positions/<int:position_id>/edit', views.edit_position, name='edit_position'),
    path('employees/', views.employees, name='employees'),
    path('employees/new/', views.new_employee, name='new_employee'),
    path('employees/<int:employee_id>/edit', views.edit_employee, name='edit_employee'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
]

