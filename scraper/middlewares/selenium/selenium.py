
import os

from scrapy.exceptions import IgnoreRequest

from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from selenium import webdriver


class SeleniumMiddleware(object):

    def process_request(self, request, spider):
        if spider.use_selenium():
            driver = SeleniumDriver(
                request.meta.get('proxy', None),
                request.meta['site_settings'].headless
            ).driver
            cookies = request.meta['site_settings'].cookies
            if len(cookies) >= 1:
                # Selenium can only add cookies to
                # the domain that it is already on
                driver.get(request.url)
                driver.delete_all_cookies()
                for cookie in cookies:
                    driver.add_cookie(cookie)
            try:
                driver.get(request.url)
            except TimeoutException:
                raise IgnoreRequest()
            self._wait_for_page(driver, spider, request)
            return HtmlResponse(
                driver.current_url,
                body=driver.page_source,
                encoding='UTF-8',
                request=request
            )

    def _wait_for_page(self, driver, spider, request):
            #
            # Make Selenium wait for a pre-specified selector
            # TODO: Specify these cases through settings file?
            #
            if spider.name == 'CDW' and request.meta['type'] == 'search':
                try:
                    driver.find_element_by_class_name('search-results-for')
                except:
                    pass
            if spider.name == 'NSIT' and request.meta['type'] == 'search':
                try:
                    driver.find_element_by_css_selector('#buy-counter')
                    driver.find_element_by_css_selector('.select-prod')
                except:
                    pass
            if spider.name == 'NSIT' and request.meta['type'] == 'item':
                try:
                    driver.find_element_by_css_selector('.prod-price')
                except:
                    pass
            if spider.name == 'STAPLES' and request.meta['type'] == 'search':
                try:
                    driver.find_element_by_css_selector(
                        'body > div.stp--container-sm.no-results > h1')
                except:
                    pass
            if spider.name == 'ESND' and request.meta['type'] == 'search':
                try:
                    driver.find_element_by_css_selector(
                        'div.ess-product-desc')
                except:
                    pass
            if spider.name == 'ESND' and request.meta['type'] == 'item':
                try:
                    driver.find_element_by_css_selector(
                        'div.ess-product-price')
                except:
                    pass
            if spider.name == 'ZORO' and request.meta['type'] == 'search':
                try:
                    driver.find_element_by_css_selector(
                        '#grid')
                except:
                    pass
            if spider.name == 'ZORO' and request.meta['type'] == 'item':
                try:
                    driver.find_element_by_css_selector(
                        '#avl-info-icon')
                except:
                    pass
            if spider.name == 'MM' and request.meta['type'] == 'item':
                try:
                    driver.find_element_by_css_selector(
                        'h3.header-primary--pd')
                except:
                    pass


class SeleniumDriver:

    def __init__(self, proxy=None, headless=True):
        options = webdriver.ChromeOptions()
        if proxy:
            options.add_argument('--proxy-server={}'.format(proxy))
            print('-' * 100)
            print('Selenium using proxy: {}'.format(proxy))
            print('-' * 100)
        if headless:
            options.add_argument('headless')
        self._driver = webdriver.Chrome(
            '{}/../../../utilities/chromedriver'.format(
                os.path.dirname(os.path.realpath(__file__))),
            chrome_options=options)
        self._driver.set_page_load_timeout(90)
        self._driver.implicitly_wait(60)

    @property
    def driver(self):
        return self._driver
