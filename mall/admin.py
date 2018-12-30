from django.contrib import admin
from .models import Product, Product_Color, Customer, Gift, Review, Banner, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'on_sale', 'device_image_file', 'created_at', 'updated_at']
    list_display_links = ['device_name']

@admin.register(Product_Color)
class Product_ColorAdmin(admin.ModelAdmin):
    list_display = ['combi_name', 'on_sale',  'color_code', 'color_modified_code', 'created_at', 'updated_at']
    list_display_links = ['combi_name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_ktshop_id',  'customer_telnum', 'created_at', 'updated_at']
    list_display_links = ['customer_name']

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ['gift_name', 'on_promotion']
    list_display_links = ['gift_name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id']
    list_display_links = ['review_id']

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_label']
    list_display_links = ['banner_label']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'order_device', 'cfmd', 'cncl', 'expd', 'device_send_date', 'gift_order_date']
    list_display_links = ['customer_name']
