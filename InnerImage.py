# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from selenium import webdriver
import os
import urllib.request

# ChromeDriver로 접속, 자원 로딩시간 1초
try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome('C:\chromedriver', options=options)
    driver.implicitly_wait(1)
    driver.refresh()
except:
    print("크롬드라이버 연결 에러")


cred = credentials.Certificate(
    'jyangca0120-firebase-adminsdk-bnprp-a39ce26b3c.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'jyangca0120',
})

db = firestore.client()

places = ['마담 티라미수 ', '빌리프커피로스터스', '몽카페그레고리']
for place in places:
    baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
    crawl_num = 20
    quotePlus = "+내부+사진"
    url = baseUrl + "\"" + place + "\"" + quotePlus
    print(url)
    driver.get(url)
    sleep(2)

    req = driver.page_source
    soup = bs(req, 'html.parser')
    images = soup.find_all(class_="_image _listImage")

    try:
        # 이미지 폴더 생성
        os.chdir('C:/Users/yjsm1/Desktop/InnerImage/')
        os.mkdir(place)
        os.chdir('C:/Users/yjsm1/Desktop/InnerImage/{}'.format(place))
    finally:
        n = 1
        for i in images:
            print("DB POST: ", n)
            imgUrl = i['src']
            try:
                db_ref = db.collection(u"Place DB").document(place)
                db_ref.update({u"photo_inside_{}".format(n): imgUrl})
            except:
                print("DB에러")
                continue

            # 매장 이름 별 폴더 생성, 내부 사진 저장

            imgUrl = i['src']
            with urllib.request.urlopen(imgUrl) as f:
                with open(place + " 내부 사진" + str(n)+'.jpg', 'wb') as h:  # w - write b - binary
                    images = f.read()
                    h.write(images)
                    print("Image Save: ", n)
            n += 1
            if n > crawl_num:
                break
