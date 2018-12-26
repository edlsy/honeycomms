from django.urls import path
from . import views

urlpatterns = [
    path('', views.mall_product_list, name='mall'),
    path('init/', views.mall_product_list_init, name='mall_init'),
]