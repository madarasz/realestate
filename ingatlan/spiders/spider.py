from ingatlan.items import IngatlanItem

from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider
from scrapy_splash import SplashRequest
from scrapy.spiders import Rule

class IngatlanLinkSpider(CrawlSpider):
    name = "Link"
    allowed_domains = ["ingatlan.com"]
    start_urls = [
        "http://ingatlan.com/listasz/elado+lakas+tegla-epitesu-lakas+xiii-ker"
    ]

    rules = (
         Rule(LinkExtractor(restrict_xpaths="//a[contains(@class,'rowclick')]"), callback="parse_link"),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='button next']"),),
    )

    def parse_link(self, response):
        yield SplashRequest(
            response.url,
            self.parse_ingatlan,
            endpoint='render.json',
            args={
                'har': 1,
                'html': 1,
            }
        )

    def parse_ingatlan(self, response):
        item = IngatlanItem()

        item['id'] = response.xpath("//b[@class='listing-id']/text()").extract_first()
        item['cim'] = response.xpath('//h1/text()').extract_first()
        item['tipus'] = response.xpath("//div[@class='listing-subtype']/text()").extract_first()
        item['terulet'] = self.process_terulet(
            response.xpath("//div[contains(@class, 'parameter-area-size')]/span[2]/text()").extract_first())
        item['szobak'] = self.process_szobak(
            response.xpath("//div[contains(@class, 'parameter-room')]/span[2]/text()").extract_first())
        item['ar'] = self.process_ar(
            response.xpath("//div[contains(@class, 'parameter-price')]/span[2]/text()").extract_first())

        item['allapot'] = response.xpath("//td[contains(text(),'llapota')]/../td[2]/text()").extract_first()
        item['komfort'] = response.xpath("//td[contains(text(),'Komfort')]/../td[2]/text()").extract_first()
        item['emelet'] = response.xpath("//td[contains(text(),'Emelet')]/../td[2]/text()").extract_first()
        item['szintek'] = response.xpath("//td[contains(text(),'szintjei')]/../td[2]/text()").extract_first()
        item['lift'] = response.xpath("//td[contains(text(),'lift')]/../td[2]/text()").extract_first()
        item['belmagassag'] = response.xpath("//td[contains(text(),'Belmagass')]/../td[2]/text()").extract_first()
        item['futes'] = response.xpath("//td[contains(text(),'F\u0171t')]/../td[2]/text()").extract_first()
        item['legkondi'] = response.xpath("//td[contains(text(),'gkondicion')]/../td[2]/text()").extract_first()

        item['akadaly'] = response.xpath("//td[contains(text(),'lymentes')]/../td[2]/text()").extract_first()
        item['wc'] = response.xpath("//td[contains(text(),'s WC')]/../td[2]/text()").extract_first()
        item['tajolas'] = response.xpath("//td[contains(text(),'jol')]/../td[2]/text()").extract_first()
        item['kilatas'] = response.xpath("//td[contains(text(),'Kil')]/../td[2]/text()").extract_first()
        item['kert'] = response.xpath("//td[contains(text(),'Kertkapcsolatos')]/../td[2]/text()").extract_first()
        item['tetoter'] = response.xpath("//td[contains(text(),'Tet\u0151t')]/../td[2]/text()").extract_first()
        item['parkolas'] = response.xpath("//td[contains(text(),'Parkol')]/../td[2]/text()").extract_first()
        item['erkely'] = self.process_terulet(
            response.xpath("//td[contains(text(),'Erk')]/../td[2]/text()").extract_first(default='0'))

        # item['mezok'] = response.xpath("//div[@class='paramterers']/table/tbody/tr/td[1]/text()").extract()

        for key, value in item.items():
            if isinstance(value, str) and value.isnumeric():
                item[key] = int(value)
            if value == 'nincs megadva' or value == None:
                item[key] = ''

        yield item

    def process_terulet(self, text):
        return int(text.split()[0].split('.')[0])

    def process_ar(self, text):
        return int(float(text.split()[0].replace(',', '.')) * 1000000)

    def process_szobak(self, text):
        splits = text.split()
        if len(splits) > 1:
            if splits[1] == '+':
                return [int(splits[0]), int(splits[2])]
            else: return text
        else: return int(splits[0])
