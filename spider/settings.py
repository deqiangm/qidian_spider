# -*- coding: utf-8 -*-

BOT_NAME = 'qidian'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

ITEM_PIPELINES = {
   'spider.pipelines.SpiderPipeline':1,
}

MYSQL_INFO = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': 'jitui1234',
    'db': 'book',
    'charset': 'utf8'
}

SQLITE_FILE = 'spider/data/result.db'

