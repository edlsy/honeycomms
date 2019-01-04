from django.contrib import admin
from .models import Product, Product_Color, Customer, Gift, Review, Banner, Order


class Product_ColorInline(admin.TabularInline):
    model = Product_Color
    verbose_name = "색상정보"
    verbose_name_plural = "색상정보"
    fields = ('color_name', 'color_code', 'color_modified_name', 'color_modified_code', "on_sale")
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['device_name', 'device_code']
    fieldsets = [
        ('기종정보', {'fields': ['device_name', 'device_code', 'device_price', 'device_image_url', 'device_image_file',
                             'ktshop_link', 'on_sale']}),
    ]
    inlines = [Product_ColorInline]
    list_display = ['device_name', 'on_sale', 'device_image_file', 'created_at', 'updated_at']
    list_display_links = ['device_name']

'''
class Product_ColorAdmin(admin.ModelAdmin):
    list_display = ['combi_name', 'on_sale', 'color_code', 'color_modified_code', 'created_at', 'updated_at']
    list_display_links = ['combi_name']
'''

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_ktshop_id',  'customer_telnum', 'created_at', 'updated_at']
    list_display_links = ['customer_name']

class GiftAdmin(admin.ModelAdmin):
    list_display = ['gift_name', 'on_promotion']
    list_display_links = ['gift_name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id']
    list_display_links = ['review_id']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_label']
    list_display_links = ['banner_label']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'order_device', 'cfmd', 'cncl', 'expd', 'device_send_date', 'gift_order_date']
    list_display_links = ['customer_name']


admin.site.register(Product, ProductAdmin)
#admin.site.register(Product_Color, Product_ColorInline)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Gift, GiftAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Order, OrderAdmin)