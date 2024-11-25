from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.sales_form, name='sales_form'),
    path('upload/', views.upload_file, name='upload_file'),
    path('list/', views.sales_list, name='sales_list'),
]
