# -*- coding: utf-8 -*-

import hashlib
import scrapy
import json
from scrapy.exceptions import DropItem
import sqlite3

class SpiderPipeline(object):

    def open_spider(self, spider):
        self.conn = sqlite3.connect(spider.settings['SQLITE_FILE'])
        self.cursor = self.conn.cursor()
        self.prepare_table()

    def prepare_table(self):
        sql_qd_book = '''CREATE TABLE IF NOT EXISTS `qd_book` (
            `qd_book_id` int(11) NOT NULL PRIMARY KEY,
            `qd_book_name` varchar(45) NOT NULL,
            `qd_book_img_url` varchar(128) DEFAULT NULL,
            `qd_book_author` varchar(45) NOT NULL,
            `qd_book_intro` text,
            `qd_book_catalog` text,
            `qd_book_tags` varchar(256) DEFAULT NULL,
            `create_time` datetime DEFAULT NULL,
            `refresh_time` datetime DEFAULT NULL
            )'''

        sql_qd_book_honors ='''CREATE TABLE IF NOT EXISTS `qd_book_honors` (
            `qd_book_id` int(11) NOT NULL PRIMARY KEY,
            `qd_book_honor` text NOT NULL,
            `create_time` datetime DEFAULT NULL
            )'''

        sql_qd_book_month_ticket = '''CREATE TABLE IF NOT EXISTS `qd_book_month_ticket` (
            `qd_book_id` int(11) NOT NULL,
            `month_ticket_qty` int(11) DEFAULT NULL,
            `month` int(11) NOT NULL,
            `year` int(11) NOT NULL,
            `refresh_time` datetime DEFAULT NULL,
            `month_ticket_rank` int(11) DEFAULT NULL,
            PRIMARY KEY (`qd_book_id`,`year`,`month`)
            )'''

        sql_qd_book_rec_ticket = '''CREATE TABLE IF NOT EXISTS `qd_book_rec_ticket` (
            `qd_book_id` int(11) NOT NULL,
            `rec_ticket_qty` int(11) DEFAULT NULL,
            `week` int(11) NOT NULL,
            `year` int(11) NOT NULL,
            `refresh_time` datetime DEFAULT NULL,
            `rec_ticket_rank` int(11) DEFAULT NULL,
            PRIMARY KEY (`qd_book_id`,`year`,`week`)
            )'''

        sql_qd_book_reward = '''CREATE TABLE IF NOT EXISTS `qd_book_reward` (
            `qd_book_id` int(11) NOT NULL,
            `reward` int(11) DEFAULT NULL,
            `week` int(11) NOT NULL,
            `year` int(11) NOT NULL,
            `refresh_time` datetime DEFAULT NULL,
            PRIMARY KEY (`qd_book_id`,`year`,`week`)
            )'''

        try:
            self._execute(sql_qd_book)
            self._execute(sql_qd_book_honors)
            self._execute(sql_qd_book_month_ticket)
            self._execute(sql_qd_book_rec_ticket)
            self._execute(sql_qd_book_reward)
        except BaseException as e:
            print('create table failed: ', )

    def process_item(self, item, spider):
        try:
            print('###############start process_item')
            sql_insert = 'INSERT OR REPLACE INTO qd_book(qd_book_id,qd_book_name,qd_book_img_url,qd_book_author,qd_book_intro,' \
                         'qd_book_catalog,qd_book_tags,create_time,refresh_time) VALUES (?,?,?,?,?,?,?,datetime("now", "localtime"),datetime("now", "localtime")) '
            self.cursor.execute(sql_insert, (item['id'], item['name'], item['img_url'], item['author'], item['intro'],
                                             item['catalog'], item['tags']))

            sql_insert= 'INSERT OR REPLACE INTO qd_book_month_ticket(qd_book_id,month_ticket_qty,month_ticket_rank,month,year,refresh_time) ' \
                        'VALUES (?,?,?,?,?,datetime("now", "localtime"))'
            month_ticket = item['month_ticket']
            self.cursor.execute(sql_insert, (item['id'], month_ticket['ticket_qty'], month_ticket['rank'], month_ticket['month'],
                                             month_ticket['year']))

            sql_insert = 'INSERT OR REPLACE INTO qd_book_rec_ticket(qd_book_id,rec_ticket_qty,rec_ticket_rank,week,year,refresh_time) ' \
                         'VALUES (?,?,?,?,?,datetime("now", "localtime"))'
            rec_ticket = item['rec_ticket']
            self.cursor.execute(sql_insert,
                                (item['id'], rec_ticket['ticket_qty'], rec_ticket['rank'], rec_ticket['week'],
                                 rec_ticket['year']))

            sql_insert = 'INSERT OR REPLACE INTO qd_book_reward(qd_book_id,reward,week,year,refresh_time) ' \
                         'VALUES (?,?,?,?,datetime("now", "localtime"))'
            reward = item['reward']
            self.cursor.execute(sql_insert,
                                (item['id'], reward['reward'], reward['week'],
                                 reward['year']))

            self.conn.commit()
            return item
        except BaseException as e:
            print('process_item failed', e)
            return None

    def _execute(self, sql_query, values=[]):
        dbcur = self.cursor
        dbcur.execute(sql_query, values)
        return dbcur

    def close_spider(self, spider):
        self.conn.close()