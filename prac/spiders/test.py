import scrapy
from scrapy import Spider
from .. import items
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse  # 추가
import time
import json

class StockSpider(Spider):
    name = 'test'
    IPO_list = []

    def start_requests(self):
        #url = "https://shop.11st.co.kr/stores/641053/category"
        url = "https://shop.11st.co.kr/stores/724098/category?isCategory=true&dispCtgrNo=1001452&categoryType=DISPLAY&largeCtgrNo=1001452"
        yield scrapy.Request(url, self.parse_start)

    def parse_start(self, response):
        result = {}
        excel = []
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
       #driver.get("https://shop.11st.co.kr/stores/641053/category")
        driver.get("https://shop.11st.co.kr/stores/641053/category")

        while True:
            try:
                moreContent = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/a")
                moreContent.click()
                time.sleep(0.2)
            except:
                break

        time.sleep(1)
        page_source = driver.page_source

        url = "https://shop.11st.co.kr/stores/641053/category"

        temp = HtmlResponse(url=url, body=page_source, encoding='utf-8')

        for index in range(1,10067):
            result = {}
            exclude = ","
            link = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/@href').get()
            result['link'] = link
            fee = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[1]/text()').get()
            if fee != "무료배송":
                name = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a[@data-log-body]/@data-log-body').get()
                name = json.loads(name)
                name = name.get('content_name',None)
                result['name'] = name
                result['fee'] = ""
                delivery = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[3]/a/div[2]/span[2]/em/span/text()').get()
                if delivery != "오늘발송":
                    result['delivery'] = ""
                    old_price = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em/text()').get()
                    new_price = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em/text()').get()
                    if new_price != None:
                        old_price = int(old_price.replace(exclude,""))
                        new_price = int(new_price.replace(exclude,""))
                        discount = ((old_price- new_price)/ old_price ) * 100
                        discount = round(discount,1) 
                        result['old_price'] = old_price
                        result['new_price'] = new_price
                        result['discount'] = str(discount) + "%" 
                    else:
                        result['old_price'] = old_price
                        result['new_price'] = old_price
                        result['discount'] = "0.0%"
                        continue
                else:
                    old_price = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em/text()').get()
                    new_price = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em/text()').get()
                    if new_price != None:
                        old_price = int(old_price.replace(exclude,""))
                        new_price = int(new_price.replace(exclude,""))
                        discount = ((old_price- new_price)/ old_price ) * 100
                        discount = round(discount,1)
                        result['delivery'] = delivery
                        result['old_price'] = old_price
                        result['new_price'] = new_price
                        result['discount'] = str(discount) + "%" 
                    else:
                        result['old_price'] = old_price
                        result['new_price'] = old_price
                        result['discount'] = "0.0%"
                        continue
        
            else:
                name = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a[@data-log-body]/@data-log-body').get()
                name = json.loads(name)
                name = name.get('content_name',None)
                result['fee'] = fee
                result['name'] = name
                delivery = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[2]/span/text()').get()
                if delivery != "오늘발송":
                    result['delivery'] = ""
                else:
                    result['delivery'] = delivery
                old_price = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em/text()').get()
                new_price = temp.xpath(f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em/text()').get()
                if new_price != None:
                    old_price = int(old_price.replace(exclude,""))
                    new_price = int(new_price.replace(exclude,""))
                    discount = ((old_price- new_price)/ old_price ) * 100
                    discount = round(discount,1)
                    result['old_price'] = old_price
                    result['new_price'] = new_price
                    result['discount'] = str(discount) + "%"     
                else:
                    result['old_price'] = old_price
                    result['new_price'] = old_price
                    result['discount'] = "0.0%"
                    continue

        
            
            excel.append(result)
        existing_df = pd.read_excel('드림로켓 테스트.xlsx')    
        df = pd.DataFrame(excel)
        combine = pd.concat([existing_df,df],ignore_index=True)
        combine.to_excel('드림로켓 테스트.xlsx', index=False)
        
