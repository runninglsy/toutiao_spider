import scrapy
from selenium import webdriver
import time
import numpy as np
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = "zzzs"
    
    def start_requests(self):
        search_result_url = 'https://www.toutiao.com/search/?keyword=%E8%87%AA%E4%B8%BB%E6%8B%9B%E7%94%9F'
        driver=webdriver.Edge()
        driver.get(search_result_url)
        time.sleep(3)
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(np.random.randint(3, 6))
        
        url_tails = Selector(text=driver.page_source).css(
                    '.rbox').re(r'a class="link title" href="(\S+)"')
        url_head = 'https://www.toutiao.com'
        driver.quit()
        for url_tail in url_tails:
            yield scrapy.Request(url=url_head+url_tail, callback=self.parse)

    def parse(self, response):
        title = response.css('.article-title::text').extract_first()
        content = ''.join(response.css('.article-content p::text').extract())
        if title is not None and content != '':
            yield {"title":title, "content":content, "url":response.url}
