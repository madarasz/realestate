from ingatlan.items import IngatlanItem

from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy_splash import SplashRequest

class IngatlanLinkSpider(CrawlSpider):
    name = "Link"
    allowed_domains = ["ingatlan.com"]
    start_urls = [
        "http://ingatlan.com/lista/elado+lakas+xiii-ker"
    ]

    def parse(self, response):
        le = LinkExtractor(allow="", restrict_xpaths="//a[contains(@class,'rowclick')]", unique=True)
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parseIngatlan,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parseIngatlan(self, response):
        item = IngatlanItem()
        item['cim'] = response.xpath('//h1/text()').extract()
        item['terulet'] = response.xpath("//div[contains(@class, 'parameter-area-size')]/span[2]/text()").extract()
        item['szobak'] = response.xpath("//div[contains(@class, 'parameter-room')]/span[2]/text()").extract()
        item['ar'] = response.xpath("//div[contains(@class, 'parameter-price')]/span[2]/text()").extract()
        item['allapot'] = response.xpath("//div[@class='paramterers']/table[1]/tbody/tr[1]/td[2]/text()").extract()
        item['komfort'] = response.xpath("//div[contains(@class, 'paramterers')]/table[1]/tbody/tr[2]/td[2]/text()").extract()

        yield item