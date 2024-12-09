from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:pk>/', views.sales_edit, name='sales_edit'),
    path('delete/<int:pk>/', views.sales_delete, name='sales_delete'),
    path('list/', views.sales_list, name='sales_list'),
    path('add/', views.sales_form, name='sales_form'),
    path('search/', views.sales_search, name='sales_search'),
]
