# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QDBookHonor(scrapy.Field):
    honor = scrapy.Field()

class QDMonthTicket(scrapy.Field):
    ticket_qty = scrapy.Field()
    rank = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()

class QDRecTicket(scrapy.Field):
    ticket_qty = scrapy.Field()
    rank = scrapy.Field()
    week = scrapy.Field()
    year = scrapy.Field()

class QDReward(scrapy.Field):
    reward = scrapy.Field()
    week = scrapy.Field()
    year = scrapy.Field()


class QDBook(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    catalog = scrapy.Field()
    tags = scrapy.Field()

    hornor = QDBookHonor()
    month_ticket = QDMonthTicket()
    rec_ticket = QDRecTicket()
    reward = QDReward()