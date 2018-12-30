from django import forms

from .models import Product, Product_Color, Customer, Gift, Review, Banner, Order

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('customer_name', 'customer_ktshop_id', 'customer_telnum', 'gift_name')