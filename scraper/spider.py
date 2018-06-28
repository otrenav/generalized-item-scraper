
import pandas
import scrapy

from slugify import slugify

from utilities.inputs import SearchStringsCSV
from utilities.select import select
from .parsers import Item, Search


class Spider(scrapy.Spider):

    errors = []

    def __init__(self, settings={}, now=None, **kwargs):
        self.now = now
        self.name = settings.name
        self.site_settings = settings
        super().__init__(**kwargs)

    def closed(self, spider):
        errors_df = pandas.DataFrame(self.errors)
        errors_df.to_csv(self._file_name('csv', appendix='_errors'))

    def start_requests(self):
        for combination in self._start_combinations():
            ss = combination['search_string']
            if self.site_settings.use_search:
                yield scrapy.Request(
                    combination['url'],
                    callback=self._parse_searches,
                    errback=self._parse_search_error(ss),
                    cookies=self.site_settings.cookies,
                    meta=self._meta('search', ss)
                )
            else:
                yield scrapy.Request(
                    combination['url'],
                    callback=self._parse_item,
                    errback=self._parse_item_error(ss),
                    cookies=self.site_settings.cookies,
                    meta=self._meta('item', ss)
                )

    def _parse_searches(self, response):
        if self._auto_redirection_detected(response):
            yield self._parse_item_with_return(response)
        elif self._double_hop_detected(response):
            yield self._parse_double_hop(response)
        else:
            selectors = self.site_settings.first_item_selectors
            if selectors:
                key = self.site_settings.first_item_selectors_key
                for i, selector in enumerate(selectors):
                    first_item = select(response, key, selector).extract_first()
                    if first_item:
                        ss = response.meta['custom_variables']['search_string']
                        yield scrapy.Request(
                            self._enforce_absolute_url(first_item),
                            callback=self._parse_item,
                            errback=self._parse_item_error(ss),
                            cookies=self.site_settings.cookies,
                            meta=self._meta('item', ss)
                        )
                        break
            yield self._parse_search(response)

    def _double_hop_detected(self, response):
        return self._content_exists(
            response,
            self.site_settings.double_hop_key,
            self.site_settings.double_hop_selectors
        )

    def _auto_redirection_detected(self, response):
        return self._content_exists(
            response,
            self.site_settings.auto_redirected_key,
            self.site_settings.auto_redirected_selectors
        )

    def _content_exists(self, response, key, selectors):
        return True if self._content(response, key, selectors) else False

    def _content(self, response, key, selectors):
        if selectors:
            for selector in selectors:
                results = select(response, key, selector).extract()
                if results:
                    return results
        return []

    def _enforce_absolute_url(self, url):
        if not url.startswith(('http', 'https')) or url.startswith('/'):
            url = '{}{}'.format(self.site_settings.base_url, url)
        return url

    def _parse_double_hop(self, response):
        links = self._content(
            response,
            self.site_settings.double_hop_key,
            self.site_settings.double_hop_selectors
        )
        ss = response.meta['custom_variables']['search_string']
        return scrapy.Request(
            self._enforce_absolute_url(links[0]),
            callback=self._parse_searches,
            errback=self._parse_search_error(ss),
            cookies=self.site_settings.cookies,
            meta=self._meta('search', ss, double_hop=True)
        )

    def _parse_item_with_return(self, response):
        self._save_html(response, '_item')
        return Item(response, self.site_settings).data()

    def _parse_item(self, response):
        self._save_html(response, '_item')
        yield Item(response, self.site_settings).data()

    def _parse_search(self, response):
        self._save_html(response, '_search')
        return Search(response, self.site_settings).data()

    def _parse_item_error(self, search_string):
        def _parse_item_error_internal(response):
            self._save_html(response, '_item')
            self.errors.append(Item(
                response,
                self.site_settings,
                error=True,
                search_string=search_string
            ).data())
        return _parse_item_error_internal

    def _parse_search_error(self, search_string):
        def _parse_search_error_internal(response):
            self._save_html(response, '_search')
            self.errors.append(Search(
                response,
                self.site_settings,
                error=True,
                search_string=search_string
            ).data())
        return _parse_search_error_internal

    def _start_combinations(self):
        if self.site_settings.use_search:
            return [
                {
                    'url': self.site_settings.search_query.format(search_string),
                    'search_string': search_string
                }
                for search_string in self._search_strings()
            ]
        else:
            return [
                {
                    'url': c['url'],
                    'search_string': c['search_string']
                }
                for c in self._combinations()
            ]

    def _search_strings(self):
        return SearchStringsCSV(self.site_settings).search_strings()

    def _combinations(self):
        return SearchStringsCSV(self.site_settings).combinations()

    def _save_html(self, response, suffix=''):
        if self.site_settings.save_html and hasattr(response, "body"):
            s = response.meta['custom_variables'].get('search_string', False)
            with open(self._file_name('html', s + suffix), 'w+b') as f:
                f.write(response.body)

    def _file_name(self, extension, search_string=None, appendix=''):
        if search_string:
            return 'outputs/html/{}_{}_{}.{}'.format(
                self.name, self.now, slugify(search_string), extension)
        return 'outputs/{}_{}{}.{}'.format(
            self.name, self.now, appendix, extension)

    def _meta(self, request_type, search_string, double_hop=False):
        meta = {
            'type': request_type,
            'site_name': self.name,
            'site_settings': self.site_settings,
            'custom_variables': {
                'search_string': search_string,
                'site_name': self.name,
                'timestamp': self.now
            }
        }
        if double_hop:
            meta['custom_variables']['double_hop'] = True
        return meta

    def use_selenium(self):
        return self.site_settings.javascript
