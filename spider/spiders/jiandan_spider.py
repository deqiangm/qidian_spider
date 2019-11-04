# -*- coding: utf-8 -*-

import scrapy
from spider.items import QDBook, QDBookHonor, QDMonthTicket, QDRecTicket, QDReward
import json
from scrapy.http import Request
import datetime

defaultencoding = 'utf-8'

def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

def to_chs(src):
    return src.encode('utf-8').decode('utf-8')

class personSpider(scrapy.Spider):
    global_index = 0
    name = 'qidian'

    allowed_domains = ['qidian.com']

    url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%d'

    def start_requests(self):
        for i in range(1000):
            request_url = self.url % (i+1)
            yield Request(request_url, callback=self.parse_page)

    def parse_page(self, response):
        booklink = response.xpath('//div[@class="book-mid-info"]/h4/a/@href').extract()
        bookname = response.xpath('//div[@class="book-mid-info"]/h4/a/text()').extract()
        for i in range(len(booklink)):
            print('book name is %s, link is %s' % (to_chs(bookname[i]), booklink[i]))
            book_url = 'https:' + booklink[i]
            yield Request(book_url, meta={'name': bookname[i]}, callback=self.parse_book)

    def parse_book(self, response):
        bookimg = response.xpath('//div[@class="book-img"]/a/@href').extract()
        bookid = response.xpath('//a[@id="addBookBtn"]/@data-bookid').extract()
        bookinfo = response.xpath('//div[@class="book-info "]')
        bookname = bookinfo.xpath('//h1/em/text()').extract()
        author = bookinfo.xpath('//h1/span/a/text()').extract()
        intro = bookinfo.xpath('//p[@class="intro"]/text()').extract()

        catalog = response.xpath('//div[@class="book-intro"]/p/text()').extract()
        tags = response.xpath('//p[@class="tag-wrap"]/a/text()').extract()
        morehonor = response.xpath('//div[@class="more-honor-wrap"]/dl/dd/text()').extract()
        honor = response.xpath('//li[@class="honor"]//strong/text()').extract()

        month_ticket_qty = response.xpath('//i[@id="monthCount"]/text()').extract()
        month_ticket_rank = response.xpath('//div[@class="ticket month-ticket"]//p/text()').re(u'排名\d+')

        rewardNum = response.xpath('//i[@id="rewardNum"]/text()').extract()
        todayNum = response.xpath('//em[@id="todayNum"]/text()').extract()

        rec_ticket_qty = response.xpath('//i[@id="recCount"]/text()').extract()
        rec_ticket_rank = response.xpath('//div[@class="ticket rec-ticket hidden"]//p/text()').re(u'排名\d+')


        if len(bookimg) < 1 or len(bookid) < 1 or len(bookname) < 1 or len(author) < 1 or len(intro) < 1 or len(catalog) < 1:
            print('Error: invalid result for book: %s' % to_chs(bookname))
            return

        book = QDBook()
        book['id'] = bookid[0]
        book['name'] = to_chs(bookname[0])
        book['img_url'] = bookimg[0]
        book['author'] = to_chs(author[0])
        book['intro'] = to_chs(intro[0])
        book['catalog'] = to_chs(catalog[0])
        book['tags'] = to_chs(' '.join(tags))

        if len(month_ticket_rank) > 0 and len(month_ticket_rank) > 0:
            month_ticket = QDMonthTicket()
            month_ticket['month'] = datetime.datetime.now().month
            month_ticket['year'] = datetime.datetime.now().year
            month_ticket['ticket_qty'] = month_ticket_qty[0]
            month_ticket['rank'] = month_ticket_rank[0][2:]
            book['month_ticket'] = month_ticket

        year, week, _ = datetime.datetime.now().isocalendar()

        if len(rec_ticket_qty) > 0 and len(rec_ticket_rank) > 0:
            rec_ticket = QDRecTicket()
            rec_ticket['ticket_qty'] = rec_ticket_qty[0]
            rec_ticket['rank'] = rec_ticket_rank[0][2:]

            rec_ticket['week'] = week
            rec_ticket['year'] = year
            book['rec_ticket'] = rec_ticket

        if len(rewardNum) > 0:
            reward = QDReward()
            reward['reward'] = rewardNum[0]
            reward['week'] = week
            reward['year'] = year
            book['reward'] = reward

        yield book

