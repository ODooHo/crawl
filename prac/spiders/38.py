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

class StockSpider(Spider):
    name = 'detail'
    IPO_list = []

    def start_requests(self):
        #url = "https://shop.11st.co.kr/stores/641053/category"
        url = "https://shop.11st.co.kr/stores/641053/category?isCategory=true&dispCtgrNo=1001446&categoryType=DISPLAY&largeCtgrNo=1001446"
        yield scrapy.Request(url, self.parse_start)

    def parse_start(self, response):
        item = items.ShopItem()
        result = []
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
       #driver.get("https://shop.11st.co.kr/stores/641053/category")
        driver.get("https://shop.11st.co.kr/stores/641053/category?isCategory=true&dispCtgrNo=1001446&categoryType=DISPLAY&largeCtgrNo=1001446")

        while True:
            try:
                moreContent = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/a")
                moreContent.click()
                time.sleep(0.2)
            except:
                break
        html = driver.page_source


        # Find the total number of items and generate indices for the URLs
        for index in range(1,2084):
            url = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div/div[2]/div[3]/div/section/div[2]/ul/li[{index}]/a')
            url = url.get_attribute("href")

            yield scrapy.Request(url, self.parse_detail)
        

    def parse_detail(self, response):
        temp = {}
        df = pd.read_excel('문구_사무용품.xlsx')
        try:
            temp['name'] = response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[2]/h1/text()').get()
            temp['discount'] = response.xpath('/html/body/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/div/dl/dd/span[1]/text()').get()
        except:
            temp['discount'] = "" 

        new_df = pd.DataFrame([temp])
        combined_df = pd.concat([df,new_df])
        combined_df.to_excel('문구_사무용품.xlsx', index=False)







        