from django.db import models


# 상품 마스터 테이블
class Product(models.Model):
    device_name = models.CharField(max_length=30, primary_key=True, verbose_name="상품명")
    device_code = models.CharField(max_length=20, verbose_name="상품코드(ktshop)")
    device_price = models.CharField(max_length=10, verbose_name="가격")
    device_image_url = models.URLField(null=True, verbose_name="사진URL")
    device_image_file = models.ImageField(upload_to="device_images", null=True, blank=True)
    ktshop_link = models.CharField(max_length=200, default="", verbose_name="KTshop URL")
    on_sale = models.BooleanField(default=False, verbose_name="판매여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="변경일시")

    def __str__(self):
        return self.device_name


# 상품-색상 조합 관리 테이블
class Product_Color(models.Model):
    device_name = models.ForeignKey('Product', on_delete=models.CASCADE, null=False) # 선택 기종명
    color_name = models.CharField(max_length=20, verbose_name="색상명(KTshop)")
    color_code = models.CharField(max_length=10, verbose_name="색상코드(KTshop)")
    color_modified_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="상품색상(변경)")
    color_modified_code = models.CharField(max_length=7, null=True, blank=True, verbose_name="색상코드(변경)")
    on_sale = models.BooleanField(default=False, verbose_name="판매여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="변경일시")

    def __str__(self):
        return self.color_name


# 고객 마스터 테이블
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=50)
    customer_telnum = models.CharField(max_length=11, unique=True)
    customer_ktshop_id = models.CharField(max_length=30, blank=True)
    #recommender_telnum = models.CharField(max_length=11, blank=True)
    #recommender_telnum = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name


# 사은품 테이블
class Gift(models.Model):
    gift_name = models.CharField(max_length=50, primary_key=True)
    gift_detail = models.ImageField(upload_to="gift_images", null=True, blank=True)
    gift_shopurl = models.URLField(null=True)
    on_promotion = models.BooleanField(default=False)

    def __str__(self):
        return self.gift_name


# 주문 마스터 테이블
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    # 고객/상품 마스터 레코드가 지워져도 리뷰는 남겨놔야 하기 때문에 on_delete=models.CASCADE 대신 on_delete=models.SET_NULL로 처리
    customer_telnum = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True) # 고객 전화번호
    customer_name = models.CharField(max_length=50) # 고객 이름
    order_device = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True) # 선택 기종명
    customer_ktshop_id = models.CharField(max_length=30) # 고객 KTshop ID
    gift_name = models.ForeignKey('Gift', on_delete=models.SET_NULL, null=True) # 고객 선택 사은품명
    recommender_telnum = models.ForeignKey('self', on_delete=models.SET_NULL, null=True) # 추천인 전화번호
    device_invoice_num = models.CharField(max_length=20) # 기기 송장번호
    gift_invoice_num = models.CharField(max_length=20) # 사은품 송장번호
    memo = models.TextField() # 담당자 메모
    cfmd = models.BooleanField(default=False) # 온라인신청서 확인
    cncl = models.BooleanField(default=False) # 주문취소
    expd = models.BooleanField(default=False) # 주문만료 (다음달로 넘어가면 사은품이 바뀌므로 만료처리)
    device_send_date = models.DateField() # 기기 발송일자
    gift_order_date = models.DateField() # 사은품 주문일자
    created_at = models.DateTimeField(auto_now_add=True) # 주문일시
    updated_at = models.DateTimeField(auto_now=True) # 최근 업데이트 일시
    cancelled_at = models.DateTimeField(auto_now_add=True) # 주문취소일시

    def __str__(self):
        return self.customer_name


# 리뷰 마스터 테이블
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    # 고객/상품 마스터 레코드가 지워져도 리뷰는 남겨놔야 하기 때문에 on_delete=models.CASCADE 대신 on_delete=models.SET_NULL로 처리
    review_writer_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    review_device_name = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    review_text = models.TextField()
    review_created_at = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name


# 메인화면 배너 마스터 테이블
class Banner(models.Model):
    banner_id = models.AutoField(primary_key=True)
    banner_label = models.CharField(max_length=50)
    banner_description = models.TextField()
    banner_image_pc = models.ImageField(upload_to="banner_images")
    banner_image_mobile = models.ImageField(upload_to="banner_images")
    banner_langding_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    terminated_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.banner_label
