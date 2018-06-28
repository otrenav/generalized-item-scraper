
import pandas
import scrapy

from datetime import datetime
from pprint import pprint

BATCH_SIZE = 100
TS_FORMAT = "%Y-%m-%d-%H-%M"
HEADING = '//*[@id="CtlgPageShell_CtlgPage_Inner"]//h1//text()'
SKUS_PARTNBR_LINKS = '//*//a[@data-mcm-partnbr]/@href'
SKUS_PRICES = '//*//td[contains(@class, "ItmTblCellPrce")]//text()'


class SKUsSpider(scrapy.Spider):

    name = "skus"
    block = None
    missings = None

    def __init__(self, block=None, missings=None, **kwargs):
        if block is None and missings is None:
            raise ValueError(
                "Provide `block` number or `missings` file. " +
                "To do so use the: " +
                "$ scrapy crawl skus -a block=1 -o block_1.json OR " +
                "$ scrapy crawl skus -a missings=inputs/missings.csv -o missings.json"
            )
        if block is not None and missings is not None:
            raise ValueError("Only specify `block` or `missings` (not both).")
        if block is not None:
            self.block = int(block)
        if missings is not None:
            self.missings = missings
        super().__init__(**kwargs)

    def start_requests(self):
        if self.block is not None:
            start = 1 + (self.block - 1) * BATCH_SIZE
            end = self.block * BATCH_SIZE
            if self.block == 1:
                start += 1
            combinations = [
                {'url': 'http://www.mcmaster.com/#{}'.format(i), 'page': i}
                for i in range(start, end)
            ]
        elif self.missings is not None:
            data = pandas.read_csv(self.missings)
            combinations = [
                {'url': 'http://www.mcmaster.com/#{}'.format(i), 'page': i}
                for i in list(data.ix[:, 0])
            ]
        for c in combinations:
            yield scrapy.Request(
                url=c['url'],
                callback=self.parse,
                meta={'page': c['page']}
            )

    def parse(self, response):
        links = self._links(response)
        print('1' * 100)
        print(response.url)
        pprint(links)
        print('1' * 100)
        return {
            'timestamp': datetime.now().strftime(TS_FORMAT),
            'heading': response.xpath(HEADING).extract_first(),
            'landing': response.url,
            'links': links
        }

    def _links(self, response):
        links = response.xpath(SKUS_PARTNBR_LINKS).extract()
        prices = response.xpath(SKUS_PRICES).extract()
        if len(links) == len(prices):
            return [{
                'sku': self._sku(l),
                'url': self._url(l),
                'price_landing': prices[i]
            } for i, l in enumerate(links)]
        else:
            return [{
                'sku': self._sku(l),
                'url': self._url(l),
                'price_landing': None
            } for i, l in enumerate(links)]

    def _sku(self, link):
        return link.replace('/#', '')

    def _url(self, link):
        return 'https://www.mcmaster.com{}'.format(link)
