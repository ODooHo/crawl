import scrapy
from scrapy import Spider
from .. import items
from pymongo import MongoClient
from bs4 import BeautifulSoup
import copy

client = MongoClient('mongodb+srv://engh0205:dhwjdgh1102@stockcluster.m2fm1sr.mongodb.net/?retryWrites=true&w=majority')
db = client.test

class Spider(Spider):
    name = 'IPO'

    IPO_list = []
    

    def start_requests(self):
        url = "http://www.ipostock.co.kr/sub03/ipo04.asp?str1=2023&str2=all"
        yield scrapy.Request(url, self.parse_start)


    def parse_start(self, response):
        # Find the total number of items and generate indices for the URLs
        total = 20 * 2

        base_url = "http://www.ipostock.co.kr"
        # for index in indices:
        #     # Generate the link xpath
        for index in range(1,total,2):
            link_xpath = f'//*[@id="print"]/table[1]//tr[4]/td/table//tr[4]/td/table//tr[{index}]/td[3]/a/@href'
        
            link = response.xpath(link_xpath).get()
            if link:
                # Create the full link URL by joining base_url and link
                full_link_url = f"{base_url}{link}"
                yield scrapy.Request(full_link_url, callback=self.parse_category)


    def parse_category(self,response):
        item = items.IPOItem()
        base_url = "http://www.ipostock.co.kr/view_pg/"
        item['date'] = response.xpath('//*[@id="print"]/table//tr[5]/td/table[2]//tr[1]/td/table//tr[2]/td[1]/table//tr[3]/td[2]/text()').get().strip()
        item['ipo_Name'] = response.xpath('//*[@id="print"]/table//tr[3]/td/table//tr/td[1]/table//tr[1]/td/table//tr/td[1]/strong[1]/text()').get().strip()
        for index in range(1,5):
            xpath = f'//*[@id="print"]/table//tr[5]/td/table[1]//tr[1]/td[{index}]/a/@href'
            link = response.xpath(xpath).get()
            if link:
                if link.find('view_02') == 0:
                    full_url = f"{base_url}{link}"
                    yield scrapy.Request(full_url, callback=self.parse_holder, meta={'item': item})
                elif link.find('view_03') == 0:
                    full_url = f"{base_url}{link}"
                    yield scrapy.Request(full_url, callback=self.parse_seed, meta={'item': item})


    
    def parse_holder(self, response):
        item = response.meta['item']
        
        html = response.text
        soup = BeautifulSoup(html,'html.parser')

        strong_tags = soup.find_all('b')
        contents = [tag.get_text().strip() for tag in strong_tags]
        if contents[0] == "바로가기":
            contents = contents[1:]

        #contents[0] : 보호예수 물량 합계
        #contents[1] : 보호예수 물량 비율
        #contents[2] : 유통가능 주식 합계
        #contents[3] : 유통가능 주식 비율
        #contents[4] : 상장 주식 수 

        item['holder'] = contents
        yield item
         

    def parse_seed(self, response):
        # html = response.text
        # soup = BeautifulSoup(html,'html.parser')

        # strong_tags = soup.find_all('strong')
        # strong_contents = [tag.get_text().strip() for tag in strong_tags]
        # strong_contents = strong_contents[-3:]
        # strong_contents.append("seed")
        item = response.meta['item']
        temp = []
        cat = 14
        ind = 2


        for i in range(3):
            for j in range(3):
                result = response.xpath(f'//*[@id="print"]/table//tr[6]/td/table[2]//tr[{cat + i}]/td[{ind + j}]/text()').get().strip()
                temp.append(result)
        
        #temp[0] : 매출액(23년 반기 or 22년 말기 *제일 최신)
        #temp[1] : 매출액(22년 반기 or 초기 * 두번째 최신)
        #temp[2] : 매출액(21년 초기 or 반기 * 세번째 최신) 이하 동일
        #temp[3~5] : 영업이익
        #temp[6~8] : 당기순이익 

    
        item['seed'] = temp
        yield item

        #db.test.insert_one(dict(item))
