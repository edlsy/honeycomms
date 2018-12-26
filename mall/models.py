from django.db import models

class Product(models.Model):
    device_name = models.CharField(max_length=30, primary_key=True)
    device_code = models.CharField(max_length=20)
    device_price = models.CharField(max_length=10)
    device_image_url = models.URLField(null=True)
    device_image_file = models.ImageField(upload_to="device_images", null=True, blank=True)
    ktshop_link = models.CharField(max_length=200, default="")
    on_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.device_name

class Product_Color(models.Model):
    combi_name = models.CharField(max_length=50, primary_key=True)  #펫네임-색상명
    device_name = models.CharField(max_length=30)
    color_name = models.CharField(max_length=20)
    color_code = models.CharField(max_length=10)
    on_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.combi_name