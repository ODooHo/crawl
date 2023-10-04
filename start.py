import scrapy
from scrapy.crawler import CrawlerProcess
from prac.spiders import StockSpider  # 이 부분을 적절하게 수정해야 합니다.

# 스크래피 설정
settings = {
    'USER_AGENT': 'Your User Agent String',
    # 필요한 다른 스크래피 설정을 추가하세요.
}

# 크롤러 프로세스 초기화
process = CrawlerProcess(settings)

# 스파이더 추가
process.crawl(StockSpider)

# 크롤러 실행
process.start()