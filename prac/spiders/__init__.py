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
import time
import json

class StockSpider(Spider):
    name = 'base'
    IPO_list = []

    def start_requests(self):
        #url = "https://shop.11st.co.kr/stores/641053/category"
        url = "https://shop.11st.co.kr/stores/641053/category?isCategory=true&dispCtgrNo=1001316&categoryType=DISPLAY&largeCtgrNo=1001316"
        yield scrapy.Request(url, self.parse_start)

    def parse_start(self, response):
        item = items.ShopItem()
        result = []
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
       #driver.get("https://shop.11st.co.kr/stores/641053/category")
        driver.get("https://shop.11st.co.kr/stores/641053/category?isCategory=true&dispCtgrNo=1001316&categoryType=DISPLAY&largeCtgrNo=1001316")

        while True:
            try:
                moreContent = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/a")
                moreContent.click()
                time.sleep(0.2)
            except:
                break
        html = driver.page_source


        # Find the total number of items and generate indices for the URLs
        for index in range(1,130):
            temp = {}
            fee = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[1]')
            fee = fee.text
            if(fee == "무료배송"):
                temp["fee"] = "O"
                try:
                    point = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[3]/span')
                    temp["point"] = point.text
                    price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["price"] = price.text
                    delivery = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[2]/span')
                    temp["delivery"] = delivery.text
                    name = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a')
                    name = name.get_attribute("data-log-body")
                    a = json.loads(name)
                    temp["name"] = a['content_name']
                    old_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em')
                    temp["old_price"] = old_price.text
                    new_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["new_price"] = new_price.text

                except:
                    temp["point"] = ""
                    price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["price"] = price.text
                    delivery = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[2]/span')
                    temp["delivery"] = delivery.text
                    name = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a') 
                    name = name.get_attribute("data-log-body")
                    a = json.loads(name)
                    temp["name"] = a['content_name']
                    old_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em')
                    temp["old_price"] = old_price.text
                    new_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["new_price"] = new_price.text

            else:
                temp["fee"] = "X"
                try:
                    point =  driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[2]/span')
                    price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    delivery = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em[1]/span')   
                    temp["point"] = point.text
                    temp["price"] = price.text
                    temp["delivery"] = delivery.text
                    name = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a')
                    name = name.get_attribute("data-log-body")
                    a = json.loads(name)
                    temp["name"] = a['content_name']
                    old_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em')
                    temp["old_price"] = old_price.text
                    new_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["new_price"] = new_price.text
                except:
                    temp["point"] = ""
                    price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["price"] = price.text
                    delivery = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[2]/em/span')
                    temp["delivery"] = delivery.text
                    name = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a')
                    name = name.get_attribute("data-log-body")
                    a = json.loads(name)
                    temp["name"] = a['content_name']
                    old_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[1]/em')
                    temp["old_price"] = old_price.text
                    new_price = driver.find_element(By.XPATH,f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a/div[2]/span[1]/span[2]/em')
                    temp["new_price"] = new_price.text
            

            result.append(temp)
        # print(result)
        df = pd.DataFrame(result)

        df.to_excel('여성신발.xlsx', index=False)
    #def parse_se"price"
        