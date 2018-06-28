
import numpy
import pandas

from urllib.parse import urlparse, parse_qs


def add_search_string(data):
    def extract_search_string(url):
        return parse_qs(urlparse(url).query).get('keywords', [])[0]
    data['search_string'] = data['url'].apply(extract_search_string)
    return data


def prepend_domain_to_brand_link(data):
    data['brand_link'] = 'https://amazon.com' + data['brand_link']
    return data


def remove_from_fast_track_learn_more_to_end(data):
    def get_first_part(string):
        if string:
            parts = string.split('Learn more')
            return ' '.join(parts[0].split())
        return ''
    data['fast_track'] = data['fast_track'].apply(get_first_part)
    return data


def keep_only_numeric_n_sellers(data):
    # NOTE: There are items for which no listed price exists, but this field
    # does contain price information (coming from other sellers). We could use
    # these prices as the listed price, but Mike must approve before I do.
    def get_number_in_parenthesis(string):
        if string:
            try:
                string = int(string.split('(')[1].split(')')[0])
            except IndexError:
                pass
        return string
    data['n_resellers'] = data['n_resellers'].apply(get_number_in_parenthesis)
    return data


FILE = 'Amazon_2018-01-15-15-38'

data = pandas.read_csv('../outputs/{}.csv'.format(FILE))
data = data.replace(numpy.nan, '', regex=True)
data = add_search_string(data)
data = prepend_domain_to_brand_link(data)
data = remove_from_fast_track_learn_more_to_end(data)
data = keep_only_numeric_n_sellers(data)

data.to_csv('../outputs/{}_clean.csv'.format(FILE), index=False)
