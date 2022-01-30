# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from selenium import webdriver


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
    'C:\\jyangca0120-firebase-adminsdk-bnprp-a39ce26b3c.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'jyangca0120',
})

db = firestore.client()

places = ['이몸이만든빵', '몽카페그레고리', '야마뜨', '빌리프커피로스터스', '오흐뒤구떼', '카페비하인드', '콜린', '발리슈퍼스토어', '달의다락', '가제트술집', '카에루', '개화기요정', '젠틀서퍼', '로원', 'Anti Cafe 손과얼굴', '티12', '크래머리', '퓨전선술집', '심양양꼬치', '쿠이신보', '술개구리', '페페로니', '카즈', '미담진족', '로칸다몽로', '비앤비', '서울브루어리', '발리슈퍼스토어', '달의다락', '더드링크', '더캐스크', '깐부치킨', '호맥', 'Fee5', '빠리쌀롱', '젠틀서퍼', '마녀커리크림치킨', '스케브루', '깐부치킨', '철인7호', '크래머리', '어반플랜트', '럭키인디아', '브루하임', '컬투치킨',
          '만평', '서울브루어리', '소문', '더페이머스버거', '몬스터브레드', '맥도날드', '콘크리트엔젤', '뚜아에모아', '번트 오렌지', '1993 버거', '플래닛61', '뉴욕아파트먼트', '바비브로스 버거앤쉐이크', '뉴욕아파트먼트오리지날그릴', '테이크잇이지', '카페리맨즈', '샌디비치 베이크하우스', '낮인더무드', '램프 샌드위치', '블리스버거', '서브웨이', '콜린', '피자네버슬립스', '키친485', '팔로피자', '몰토베네', '비볼리', '아우룸', '토파', '더피자보이즈', '첸토페르첸토', '오리지널시카고피자', 'D_51', '더그리드', '더플레이스', '빠넬로', '카밀로라자네리아', '오스테리아샘킴', '스파카나폴리', '로칸다몽로', '로로11', '홍대화덕피자']
for place in places:
    baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
    crawl_num = 10
    quotePlus = "+메뉴판"
    url = baseUrl + "\"" + place + "\"" + quotePlus
    print(url)
    driver.get(url)
    sleep(2)

    req = driver.page_source
    soup = bs(req, 'html.parser')
    images = soup.find_all(class_="_image _listImage")

    n = 1
    for i in images:
        print(n)
        imgUrl = i['src']
        try:
            db_ref = db.collection(u"강남역").document(place)
            db_ref.update({u"photo_inside_{}".format(n): imgUrl})
        except:
            print("DB에러")
        n += 1
        if n > crawl_num:
            break
