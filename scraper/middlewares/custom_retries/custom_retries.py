
from utilities.select import select

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class CustomRetriesMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        # This is standard Scrapy code for `process_response()`
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        # This is our own added check
        reason = self._should_be_retried_reason(request, response)
        if reason != '':
            return self._retry(request, reason, spider) or response
        return response

    def _should_be_retried_reason(self, request, response):
        """Return '' if request should not be retried"""
        if request.meta['site_name'] != 'Amazon':
            return ''
        # if request.meta['type'] == 'search':
        #     if not self._number_of_results_data_exists(request, response):
        #         return 'Empty `number_of_results` data'
        return ''

    def _number_of_results_data_exists(self, request, response):
        site_settings = request.meta['site_settings']
        key = 'number_of_results'
        for selector in site_settings.search_fields[key]:
            raw_text = self._raw_text(response, key, selector)
            if raw_text:
                raw_text = raw_text.encode("ascii", errors="ignore").decode()
                if len(raw_text) > 0:
                    return True
        return False

    def _raw_text(self, response, key, selector):
        texts_list = select(response, key, selector).extract()
        return ' '.join(' '.join(texts_list).split()) if texts_list else []
