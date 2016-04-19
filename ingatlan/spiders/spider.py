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
                self.parse_ingatlan,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parse_ingatlan(self, response):
        item = IngatlanItem()

        item['cim'] = response.xpath('//h1/text()').extract_first()
        item['tipus'] = response.xpath("//div[@class='listing-subtype']/text()").extract_first()
        item['terulet'] = self.process_terulet(
            response.xpath("//div[contains(@class, 'parameter-area-size')]/span[2]/text()").extract_first())
        item['szobak'] = self.process_szobak(
            response.xpath("//div[contains(@class, 'parameter-room')]/span[2]/text()").extract_first())
        item['ar'] = self.process_ar(
            response.xpath("//div[contains(@class, 'parameter-price')]/span[2]/text()").extract_first())

        item['allapot'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[1]/td[2]/text()").extract_first()
        item['komfort'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[2]/td[2]/text()").extract_first()
        item['emelet'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[3]/td[2]/text()").extract_first()
        item['szintek'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[4]/td[2]/text()").extract_first()
        item['lift'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[5]/td[2]/text()").extract_first()
        item['belmagassag'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[6]/td[2]/text()").extract_first()
        item['futes'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[7]/td[2]/text()").extract_first()
        item['legkondi'] = response.xpath(
            "//div[@class='paramterers']/table[1]/tbody/tr[8]/td[2]/text()").extract_first()

        item['akadaly'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[1]/td[2]/text()").extract_first()
        item['wc'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[2]/td[2]/text()").extract_first()
        item['tajolas'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[3]/td[2]/text()").extract_first()
        item['kilatas'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[4]/td[2]/text()").extract_first()
        item['kert'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[5]/td[2]/text()").extract_first()
        item['tetoter'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[6]/td[2]/text()").extract_first()
        item['parkolas'] = response.xpath(
            "//div[@class='paramterers']/table[2]/tbody/tr[7]/td[2]/text()").extract_first()

        for key, value in item.items():
            if isinstance(value, str) and value.isnumeric():
                item[key] = int(value)
            if value == 'nincs megadva':
                item[key] = ''

        yield item

    def process_terulet(self, text):
        return int(text.split()[0])

    def process_ar(self, text):
        return int(float(text.split()[0].replace(',', '.')) * 1000000)

    def process_szobak(self, text):
        splits = text.split()
        if len(splits) > 1:
            if splits[1] == '+':
                return [int(splits[0]), int(splits[2])]
            else: return text
        else: return int(splits[0])
