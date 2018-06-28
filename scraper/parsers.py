
from twisted.internet.error import TimeoutError, TCPTimedOutError
from selenium.common.exceptions import WebDriverException
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from scrapy.exceptions import IgnoreRequest
from pprint import pprint

from utilities.select import select


class Parser:

    url_type = None

    def __init__(self, response, settings, error, search_string):
        self.search_string = search_string
        self.settings = settings
        self.response = response
        self.error = error
        if self.error:
            self.url = response.request.url
            if response.check(HttpError):
                self.response_status = 'HTTP Error {}'.format(
                    response.value.response.status)
            elif response.check(DNSLookupError):
                self.response_status = 'DNS Lookup Error'
            elif response.check(TimeoutError, TCPTimedOutError):
                self.response_status = 'TCP Timeout Error'
            elif response.check(IgnoreRequest):
                self.response_status = 'Selenium Timeout Error'
            elif isinstance(response, WebDriverException):
                self.response_status = 'Selenium No-Session Error'
            else:
                raise ValueError("Is there a missing case for errors?")
            self._print_error_info()
        else:
            self.url = response.url
            self.response_status = 'HTTP {}'.format(self.response.status)

    def data(self):
        data = self._initial_data()
        if not self.error:
            for key in self.fields:
                text = ''
                for i, selector in enumerate(self.fields[key]):
                    raw_text = self._raw_text(key, selector)
                    if raw_text:
                        text = raw_text
                        i += 1
                        break
                clean_text = text.encode("ascii", errors="ignore").decode()
                data[key] = clean_text
                data["{}_selector".format(key)] = i
        return data

    def _initial_data(self):
        """Build initial data

        Can't just use `self.error` because, there may not be any metadata at
        all when `self.error` is True due to an error at the Twisted level.
        """
        if hasattr(self.response, 'meta'):
            meta = self.response.meta
            data = meta.get('custom_variables', {})
        elif hasattr(self.response.value, 'response'):
            meta = self.response.value.response.meta
            data = meta.get('custom_variables', {})
            data['Error'] = self.response_status
        else:
            data = {
                'search_string': self.search_string,
                'error': self.response_status
            }
        data[self.response_status_variable] = self.response_status
        data[self.proxy_variable] = meta.get('proxy', 'None')
        data[self.url_variable] = self.url
        return data

    def _raw_text(self, key, selector):
        texts_list = select(self.response, key, selector).extract()
        return ' '.join(' '.join(texts_list).split()) if texts_list else []

    def _print_error_info(self):
        print('!' * 100)
        print('Error:')
        print(self.error)
        print('Search string:')
        print(self.search_string)
        print('URL:')
        print(self.url)
        print('Response status:')
        print(self.response_status)
        print('Response:')
        pprint(self.response.__dict__)
        print('!' * 100)


class Item(Parser):

    def __init__(self,
                 response,
                 settings,
                 error=False,
                 search_string=''):
        self.response_status_variable = 'response_status_item'
        self.proxy_variable = 'proxy_item'
        self.url_variable = 'url_item'
        self.fields = settings.item_fields
        super().__init__(response, settings, error, search_string)


class Search(Parser):

    def __init__(self,
                 response,
                 settings,
                 returned_results=None,
                 error=False,
                 search_string=''):
        self.response_status_variable = 'response_status_search'
        self.proxy_variable = 'proxy_search'
        self.url_variable = 'url_search'
        self.returned_results = returned_results
        self.fields = settings.search_fields
        super().__init__(response, settings, error, search_string)
