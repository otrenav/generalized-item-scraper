
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

BOT_NAME = 'mcmaster_skus'
SPIDER_MODULES = ['mcmaster_skus.spiders']
NEWSPIDER_MODULE = 'mcmaster_skus.spiders'

CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 10

AUTOTHROTTLE_TARGET_CONCURRENCY = 0.1
AUTOTHROTTLE_START_DELAY = 10
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False

DOWNLOADER_MIDDLEWARES = {
    'mcmaster_skus.middlewares.UserAgentsMiddleware': 400,
    'mcmaster_skus.middlewares.SeleniumMiddleware': 950
}
