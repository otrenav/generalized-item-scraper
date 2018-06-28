
import os
import random

from selenium import webdriver

from .constants import PROXIES


class ProxiesMiddleware:

    def __init__(self):
        # self.proxies = RealTimeProxies().list()
        self.proxies = PredefinedProxies().list()

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)


class RealTimeProxies:

    """Get a US HTTPS proxies list in real-time

    Currently, the data is retrieved from proxydb.net, but
    other sites could be integrated similarly. This is necessary
    to have a fresh list of US-based proxies that we can use
    to scrape the rest of the product data.
    """

    url = 'http://proxydb.net/?protocol=https&country=US'

    table_css_selector = (
        'body > div > div.table-responsive ' +
        '> table > tbody > tr'
    )

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(
            '{}/../utilities/chromedriver'.format(
                os.path.dirname(os.path.realpath(__file__))),
            chrome_options=options
        )

    def list(self):
        print('-' * 100)
        print('GETTING FRESH LIST OF PROXIES...')
        self.driver.get(self.url)
        rows = self.driver.find_elements_by_css_selector(
            self.table_css_selector
        )
        proxies = []
        for row in rows:
            proxies.append('http://{}'.format(
                row.find_elements_by_tag_name("td")[0].text))
        print(proxies)
        print('-' * 100)
        return proxies


class PredefinedProxies:

    """Use a predefined set of proxies

    Semi-dedicated proxies from: https://blazingseollc.com/
    """

    def __init__(self):
        self.proxies = PROXIES

    def list(self):
        return self.proxies
