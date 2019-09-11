# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

from sqlalchemy.orm import sessionmaker
from getpolicy.models import Deals, db_connect, create_table


class GetpolicyPipeline(object):

    def process_item(self, item, spider):
        return item


    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


'''
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'gp_user'
        password = 'test1' # your password
        database = 'gp_db'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into scraped(Privacy, Terms, rest_url, url, fail) values(%s,%s,%s,%s,%s);",[item['Privacy'],item['Terms'], item['rest_url'], item['url'], item['fail']])
        self.connection.commit()
        return item
'''