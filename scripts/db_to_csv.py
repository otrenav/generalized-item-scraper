
from argparse import ArgumentParser
from pymongo import MongoClient
from pandas import DataFrame

DB_NAME = 'flatfooted'
DB_HOST = 'localhost'
DB_PORT = 27017

DB = MongoClient(DB_HOST, DB_PORT)
SEARCHES = DB[DB_NAME]['searches']
ITEMS = DB[DB_NAME]['items']

parser = ArgumentParser()
parser.add_argument("--date-start", help="Format: YYYY-MM-DD-hh-mm")
parser.add_argument("--date-end", help="Format: YYYY-MM-DD-hh-mm")
parser.add_argument("--search-string", help="As found in `site_id` column")
parser.add_argument("--site", help="As found in `settings.py`")
parser.add_argument("--file", help="Output CSV file name")
args = parser.parse_args()


def db_to_csv(date_start=None, date_end=None,
              search_string=None, site=None, file=None):
    check_arguments(date_start, date_end, search_string, site)
    file = "results.csv" if file is None else file
    i_query = items_query(date_start, date_end, search_string, site)
    items_cursor = ITEMS.find(i_query)
    items = DataFrame.from_records(items_cursor)
    items.to_csv(file, index=False)


def items_query(date_start, date_end, search_string, site):
    query = {}
    if date_start and date_end:
        query['timestamp'] = {"$lt": date_end, "$gt": date_start}
    if search_string:
        query['search_string'] = {"$regex": ".*{}.*".format(search_string)}
    if site:
        query['site_name'] = site
    return query


def searches_query(items, date_start, date_end, search_string, site):
    pass


def check_arguments(date_start, date_end, search_string, site):
    if date_start is not None and date_end is not None:
        check_date(date_start)
        check_date(date_end)
        date_range = True
    else:
        date_range = False
    if not date_range and not search_string and not site:
        raise ValueError("Specify one dimension to query for (see --help)")


def check_date(string):
    if False:
        raise ValueError("Date format error: YYYY-MM-DD-hh-mm")


# Run automatically after functions have been loaded
db_to_csv(
    args.date_start,
    args.date_end,
    args.search_string,
    args.site,
    args.file
)
