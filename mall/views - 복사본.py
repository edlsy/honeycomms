from django.shortcuts import render
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from django.core.files import File
import os
import requests
from .models import Product, Product_Color

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ktshop_site_url = "https://m.shop.kt.com:444/m/smart/agncyInfoView.do?vndrNo=AA01344&sortProd=SALE"

def mall_product_list(request):
    item_name = {}
    item_price = {}
    item_code = {}
    thumbs_link = {}
    color_name = {}
    color_code = {}
    #local_imgs_path = os.path.join(BASE_DIR, "mall", "static", "imgs", "device_imgs")
    #local_imgs_path = "static/imgs/device_imgs"
    #local_imgs_list = os.listdir(os.path.join(BASE_DIR,"static","imgs","device_imgs"))
    ktshop_device_url = "https://shop.kt.com/smart/productView.do?prodNo=&vndrNo=&supportType=02"
    vndr_code = "AA01344"   # 허니컴즈 대리점코드

    html = urlopen(ktshop_site_url)
    bsObj = BeautifulSoup(html, "html.parser")
    thumbs_blocks = bsObj.findAll("div", {"class": "thumbs"})
    prodInfo_blocks = bsObj.findAll("div", {"class": "prodInfo"})

    # 단말정보(기종명, 가격) 블럭수만큼 loop를 실행하면서 기종명, 가격, 기종코드를 읽어들임
    for idx, prodInfo in enumerate(prodInfo_blocks):
        item_name[idx] = prodInfo.ul.find("li", {"class": "prodName"}).text
        item_price[idx] = prodInfo.ul.find("li", {"class": "prodPrice"}).span.text
        href_value = prodInfo.ul.find("li", {"class": "prodSupport"}).findAll("a")[0].attrs['href']
        item_code[idx] = href_value[25:35]

    # 단말 이미지/색상 블럭수만큼 loop를 실행하면서 단말 이미지링크와 색상블럭을 읽어들임
    for idx, thumbs in enumerate(thumbs_blocks):
        thumbs_link[idx] = thumbs.findAll("img")[0].attrs['src']
        color_blocks = thumbs.find("ul", {"class": "optColor"}).findAll("li")
        temp_img = urlretrieve(thumbs_link[idx])

        print("***", temp_img)
        print("***", len(temp_img))
        print("***", type(temp_img))
        # 기종사진 폴더에 이 기종의 이미지 파일이 없으면, 지금 읽어들인 링크의 단말이미지를 저장
        #if (item_name[idx] + ".png") not in local_imgs_list:
        #    print("%s image file saving...\n", item_name[idx])

        # 단말색상 블럭에서 색상명과 색상값을 읽어들임 (전체 페이지의 단말색상 블럭수만큼 loop
        for idx2, color_blocks in enumerate(color_blocks):
            color_name[idx2] = color_blocks.find("span").text
            temp_color_code = color_blocks.find("span").attrs['style']
            color_code[idx2] = temp_color_code[17:24]

            # 기존 DB에 지금의 기종명+색상명과 일치하는 row가 없으면, 지금의 기종명+색상명 데이터를 Product_Color 테이블의 새로운 레코드로 추가
            if len(Product_Color.objects.filter(combi_name=item_name[idx]+"-"+color_name[idx2])) == 0:
                Product_Color(combi_name=item_name[idx]+"-"+color_name[idx2], device_name=item_name[idx],
                              color_name=color_name[idx2], color_code=color_code[idx2]).save()

        # 기존 DB에 이 기종명+가격과 일치하는 row가 없으면
        if len(Product.objects.filter(device_name=item_name[idx], device_price=item_price[idx])) == 0:

            # 기존 DB에 이 기종명과 일치하는 row가 없으면, 지금의 전체 정보(기종명,가격,코드,이미지위치)를 Product 테이블의 새로운 레코드로 추가
            if len(Product.objects.filter(device_name=item_name[idx])) == 0:
                print("%s info saving...\n", item_name[idx])
                temp_ktshop_link = ktshop_device_URL(ktshop_device_url, item_code[idx], 48, vndr_code, 56)
                print("ktshop_link : ", temp_ktshop_link)
                Product(device_name=item_name[idx], device_price=item_price[idx], device_code=item_code[idx],
                        ktshop_link=temp_ktshop_link, device_image_file=File(open(temp_img[0]))).save()

            # 기존 DB에 이 기종명과 일치하는 row가 있으면, 가격정보만 업데이트
            else:
                print("%s price updating...\n", item_name[idx])
                product = Product.objects.get(device_name=item_name[idx])
                product.device_price = item_price[idx]
                product.save()

    products = Product.objects.filter()
    product_colors = Product_Color.objects.filter()

    return render(request, 'mall/mall_main.html', {'products': products, 'product_colors': product_colors})


def ktshop_device_URL(ktshop_url, device_code, device_code_idx, vndr_code, vndr_code_idx):
    return ktshop_url[:device_code_idx] + device_code + ktshop_url[device_code_idx:vndr_code_idx] + vndr_code + ktshop_url[vndr_code_idx:]