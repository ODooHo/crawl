# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    ipoName = scrapy.Field() # 공모주 명
    ipoCode = scrapy.Field() # 종목 코드   
    owner = scrapy.Field() # 대표명
    shareholder = scrapy.Field() #최대 주주 
    locate = scrapy.Field() # 위치
    seed = scrapy.Field() # 자본금
    business = scrapy.Field() # 업종
    ipoQuantity = scrapy.Field() #공모주식수
    faceValue = scrapy.Field() #액면가
    collusion = scrapy.Field() #희망 공모가
    chief = scrapy.Field() #주간사
    compete = scrapy.Field() #기관 경쟁률
    commit = scrapy.Field() #의무 보유 확약
    date = scrapy.Field() #공모 날짜
    protect = scrapy.Field() #보호 예수 물량
    protectPercent = scrapy.Field() #보호 예수 비율
    possible = scrapy.Field() #유통 가능 물량
    possiblePercent = scrapy.Field() #유통 가능 비율
    sharedQuantity = scrapy.Field() #상장 주식 수
    sale = scrapy.Field() #매출액
    profit = scrapy.Field() #영업이익
    pureProfit = scrapy.Field() #순 이익
    finalCollusion = scrapy.Field #확정 공모가
    


class ShopItem(scrapy.Item):
    point = scrapy.Field() # 포인트
    price = scrapy.Field() # 가격 
    delivery = scrapy.Field() # 오늘 발송
    fee = scrapy.Field() # 배송비     
    discount = scrapy.Field() # 할인율     
    name = scrapy.Field() # 상품 명
    
    