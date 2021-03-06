import scrapy
from google.items import GoogleItem


class google_Spider(scrapy.Spider):
    name = "googleSearch"
    allowed_domains = []
    start_urls = []

    def __init__(self, domain='', url='', *args, **kwargs):
        super(google_Spider, self).__init__(*args, **kwargs)
        self.allowed_domains = [domain]
        self.start_urls = [url]

    def parse(self, response):
        #print response.body
        titles = response.xpath('//h3[@class="r"]/a/text()')
        urls = response.xpath('//h3[@class="r"]/a/@href')
        descriptions = response.xpath('//span[@class="st"]/text()')

        for i in range(0,len(titles)):
            item = GoogleItem()
            item['title'] = titles[i].extract().encode('utf8')
            item['link'] = urls[i].extract().encode('utf8')
            item['desc'] = descriptions[i].extract().encode('utf8')
            yield item

        href = response.urljoin(response.xpath('//a[@class="pn"]//@href').extract()[0])
        if href:
            url = response.urljoin(href)
            yield scrapy.Request(url, self.parse)
