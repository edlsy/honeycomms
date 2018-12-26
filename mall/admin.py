from django.contrib import admin
from .models import Product, Product_Color

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'on_sale', 'created_at', 'updated_at']
    list_display_links = ['device_name']

@admin.register(Product_Color)
class Product_ColorAdmin(admin.ModelAdmin):
    list_display = ['combi_name', 'on_sale',  'color_code', 'created_at', 'updated_at']
    list_display_links = ['combi_name']
