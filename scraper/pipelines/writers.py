
from pymongo import MongoClient

from settings import SETTINGS


class MongoWriterPipeline(object):

    def __init__(self):
        self.mongo_db = SETTINGS['mongo']['db']
        self.host = SETTINGS['mongo']['host']
        self.port = SETTINGS['mongo']['port']

    def open_spider(self, spider):
        self.client = MongoClient(self.host, self.port)
        self.searches = self.client[self.mongo_db]['searches']
        self.items = self.client[self.mongo_db]['items']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'url_item' in dict(item).keys():
            self.items.insert_one(dict(item))
        else:
            self.searches.insert_one(dict(item))
        return item
