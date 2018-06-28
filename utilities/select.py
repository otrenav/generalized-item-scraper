
def select(response, key, selector):
    """Method selector for a given Scrapy response object and selector

    The `key` is a string that may or may not contain '_css'. If it does, the
    CSS `selector` for the given `response` is returned, and if it doesn't the
    XPATH `selector` is returned instead.
    """
    if '_css' in key:
        return response.css(selector)
    return response.xpath(selector)
