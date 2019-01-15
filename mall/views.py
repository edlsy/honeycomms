from django.shortcuts import render
from urllib.request import urlopen
from urllib.request import urlretrieve
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.files import File
from tempfile import NamedTemporaryFile
from django.views.generic import CreateView
from .forms import OrderForm
import os
import requests
from time import sleep
from .models import Product, Product_Color, Customer, Gift, Review, Banner, Order

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ktshop_site_url = "https://m.shop.kt.com:444/m/smart/agncyInfoView.do?vndrNo=AA01344&sortProd=SALE"


# 슬러그없이 접속했을 때 기존 저장된 DB를 기반으로 KT Direct 메인화면 출력 (고객용)
def mall_product_list(request):
    print(BASE_DIR)
    print("start : ", datetime.now())
    products = Product.objects.filter(on_sale=True)
    product_colors = Product_Color.objects.filter(on_sale=True)
    print("end   : ", datetime.now())
    return render(request, 'mall/mall_main.html', {'products': products, 'product_colors': product_colors})


# 슬러그 init/으로 접속했을 때 KTshop 업데이트 내용을 새롭게 반영하여 KT Direct 메인화면 출력 (관리자용)
def mall_product_list_init(request):
    ktshop_product_name = {}
    ktshop_product_price = {}
    ktshop_product_code = {}
    ktshop_thumbs_link = {}
    ktshop_color_name = {}
    ktshop_color_code = {}
    ktshop_image_name = {}
    ktshop_product_link = {}
    ktshop_url = "https://shop.kt.com/smart/productView.do?prodNo=&vndrNo=&supportType=02"
    vndr_code = "AA01344"   # 허니컴즈 대리점코드

    html = requests.get(ktshop_site_url)
    bsObj = BeautifulSoup(html.text, "html.parser")
    thumbs_blocks = bsObj.findAll("div", {"class": "thumbs"})
    prodInfo_blocks = bsObj.findAll("div", {"class": "prodInfo"})

    # 미판매기종/색상 반영을 위해 전체 기존기종을 inactive로 설정
    print("inactive start : ", datetime.now())
    if len(Product.objects.all()) != 0:
        product = Product.objects.all()
        # print(len(product))
        for i in range(len(product)):
            # print("prdt inactive : ", datetime.now())
            product[i].on_sale = False
            product[i].save()
            # print("{} - {}".format(product[i].device_name, product[i].on_sale))
    if len(Product_Color.objects.all()) != 0:
        product_color = Product_Color.objects.all()
        for i in range(len(product_color)):
            # print("clor inactive : ", datetime.now())
            product_color[i].on_sale = False
            product_color[i].save()
    print("inactive end   : ", datetime.now())

    # 단말정보(기종명, 가격) 블럭수만큼 loop를 실행하면서 기종명, 가격, 기종코드를 읽어들임
    print("1st loop start : ", datetime.now())
    for idx, prodInfo in enumerate(prodInfo_blocks):
        ktshop_product_name[idx] = prodInfo.ul.find("li", {"class": "prodName"}).text
        ktshop_product_price[idx] = prodInfo.ul.find("li", {"class": "prodPrice"}).span.text
        href_value = prodInfo.ul.find("li", {"class": "prodSupport"}).findAll("a")[0].attrs['href']
        ktshop_product_code[idx] = href_value[25:35]
    print("1st loop end   : ", datetime.now())

    # 단말 이미지/색상 블럭수만큼 loop를 실행하면서 단말 이미지링크와 색상블럭을 읽어들임
    print("2nd loop start : ", datetime.now())

    # 단말 수만큼 loop를 실행하면서 단말 이미지링크를 읽고 단말 이미지를 저장함
    for idx, thumbs in enumerate(thumbs_blocks):
        ktshop_thumbs_link[idx] = thumbs.findAll("img")[0].attrs['src']
        color_blocks = thumbs.find("ul", {"class": "optColor"}).findAll("li")

        ktshop_product_link[idx] = get_ktshop_device_url(ktshop_url, ktshop_product_code[idx], 48, vndr_code, 56)
        ktshop_image_name[idx] = ktshop_product_name[idx] + os.path.splitext(os.path.basename(ktshop_thumbs_link[idx]))[1]
        '''
        temp_image = urlretrieve(thumbs_link[idx])
        image_name[idx] = item_name[idx] + os.path.splitext(os.path.basename(thumbs_link[idx]))[1]
        print("{} is saved.".format(image_name[idx]))
        sleep(1)
        '''

        # Product 테이블에 현재의 기종명 레코드가 없으면 새로운 레코드 저장 후 on_sale=True
        if len(Product.objects.filter(device_name=ktshop_product_name[idx])) == 0:
            Product(
                device_name = ktshop_product_name[idx],
                device_price = ktshop_product_price[idx],
                device_code = ktshop_product_code[idx],
                ktshop_link = ktshop_product_link[idx],
                device_image_url = ktshop_thumbs_link[idx],
                on_sale = True
            ).save()
            #temp_product = Product.objects.get(device_name=item_name[idx])
            #temp_product.device_image_file.save(temp_image_name, File(open(temp_image[0], 'rb')))
        # Product 테이블에 현재의 기종명 레코드가 있으면 해당 레코드에 KTshop 크롤링값을 업데이트 후 on_sale=True
        else:
            temp_product = Product.objects.get(device_name=ktshop_product_name[idx])
            temp_product.device_price = ktshop_product_price[idx]
            temp_product.device_code = ktshop_product_code[idx]
            temp_product.ktshop_link = ktshop_product_link[idx]
            temp_product.device_image_url = ktshop_thumbs_link[idx]
            #temp_product.device_image_file.save(temp_image_name, File(open(temp_image[0], 'rb')))
            temp_product.on_sale = True
            temp_product.save()

        # 단말색상 블럭에서 색상명과 색상값을 읽어들임 (전체 페이지의 단말색상 블럭수만큼 loop)
        for idx2, color_blocks in enumerate(color_blocks):
            ktshop_color_name[idx2] = color_blocks.find("span").text
            temp_color_code = color_blocks.find("span").attrs['style']
            ktshop_color_code[idx2] = temp_color_code[17:24]

            # 기존 DB에 지금의 색상명과 일치하는 row가 없으면, 지금의 색상명 데이터를 Product_Color 테이블의 새로운 레코드로 추가

            if len(Product_Color.objects.filter(device_name=ktshop_product_name[idx], color_name=ktshop_color_name[idx2]))==0:
                temp_product = Product.objects.get(device_name=ktshop_product_name[idx])
                Product_Color.objects.create(device_name=temp_product,
                    color_name=ktshop_color_name[idx2],
                    color_code=ktshop_color_code[idx2],
                    on_sale=True)

            # 현재 KTshop에 판매 중인 모든 색상에 대해 on_sale=True 설정
            temp_product_color = Product_Color.objects.get(device_name=ktshop_product_name[idx], color_name=ktshop_color_name[idx2])
            temp_product_color.on_sale = True
            temp_product_color.save()

    print("2nd loop end   : ", datetime.now())

    product_image_save(ktshop_product_name, ktshop_image_name, ktshop_thumbs_link)

    print("img save end   : ", datetime.now())

    products = Product.objects.filter(on_sale=True)
    product_colors = Product_Color.objects.filter(on_sale=True)

    return render(request, 'mall/mall_main.html', {'products': products, 'product_colors': product_colors})


# 파라미터를 조합하여 해당 단말의 KTshop URL 리턴
def get_ktshop_device_url(ktshop_url, device_code, device_code_idx, vndr_code, vndr_code_idx):
    return ktshop_url[:device_code_idx] + device_code + ktshop_url[device_code_idx:vndr_code_idx] + vndr_code + ktshop_url[vndr_code_idx:]


# Product 이미지 이름 리스트와 URL 리스트를 받아서 이미지 파일을 저장하는 함수
# 해당 product의 이미지가 이미 존재하는 경우에는 bypass
def product_image_save(item_name_list, image_name_list, image_url_list):
    existing_image_names_list = os.listdir(os.path.join(BASE_DIR,"media","device_images"))

    for idx in range(len(image_name_list)):
        temp_product = Product.objects.get(device_name=item_name_list[idx])

        # 저장된 DB에 이미지파일이 저장되어 있지 않으면 새롭게 파일 저장
        # case#1 : 해당 기종이 DB에 등록되어 있고, 이미지폴더에 이미지가 저장되어 있다면
        if (temp_product.device_image_file.name != "") and (temp_product.device_image_file.name.split("/")[1] in existing_image_names_list):
            print("{} already exists.".format(image_name_list[idx]))
            continue
            
        # case#2 : 해당 기종명으로 조회된 DB 레코드에 이미지가 저장되어 있지만 해당 기종 이미지가 이미지 폴더에 존재하지 않는다면
        try:
            temp_image = requests.get(image_url_list[idx])
        except:
            print("exception occurred. Retry~!!")
            idx-=1
            print("[retry] index = {}".format(idx))
            continue
        else:
            temp_image_file = NamedTemporaryFile(delete=True)
            temp_image_file.write(temp_image.content)
            temp_image_file.flush()
            temp_product.device_image_file.save(image_name_list[idx], File(temp_image_file))
            print("{} is just saved.".format(temp_product.device_image_file))
            temp_product.on_sale = True
            temp_product.save()


def order_new(request):
    gifts = Gift.objects.filter(on_promotion=True)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_at = timezone.now()
            order.save()
    else:
        form = OrderForm()
    if len(gifts) == 0:
        return render(request, 'mall/order.html', {'form': form})
    else:
        return render(request, 'mall/order.html', {'form': form, 'gifts': gifts})