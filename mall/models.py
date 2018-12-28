from django.db import models


# 상품 마스터 테이블
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


# 상품-색상 조합 관리 테이블
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


# 고객 마스터 테이블
class Customer(models.Model):
    customer_ktshop_id = models.CharField(max_length=30, primary_key=True)
    customer_name = models.CharField(max_length=50)
    customer_phonenumber = models.CharField(max_length=11)
    # 추천인은 null 대신 blank=True만 정의한다. 만약 추천인이 없으면 ""로 처리.
    customer_recommender = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name


# 주문 마스터 테이블
# 이 사이트에서의 주문은 리뷰작성임
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    # 고객/상품 마스터 레코드가 지워져도 리뷰는 남겨놔야 하기 때문에 on_delete=models.CASCADE 대신 on_delete=models.SET_NULL로 처리
    review_writer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    review_device = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    review_text = models.TextField()
    review_created_at = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name
