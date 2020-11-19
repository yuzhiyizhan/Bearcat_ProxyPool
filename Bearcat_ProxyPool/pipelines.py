# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import redis
import sqlite3
import pymysql
from loguru import logger
from peewee import Model
from peewee import CharField
from peewee import FloatField
from peewee import MySQLDatabase
from itemadapter import ItemAdapter
from Bearcat_ProxyPool.settings import REDIS_DB
from Bearcat_ProxyPool.settings import REDIS_HOST
from Bearcat_ProxyPool.settings import REDIS_PORT
from Bearcat_ProxyPool.settings import REDIS_PARAMS
from Bearcat_ProxyPool.settings import REDIS_MAXCONNECTIONS
from Bearcat_ProxyPool.settings import REDIS_CONNECT_TIMEOUT
from Bearcat_ProxyPool.settings import MYSQL_DB
from Bearcat_ProxyPool.settings import MYSQL_USER
from Bearcat_ProxyPool.settings import MYSQL_PORT
from Bearcat_ProxyPool.settings import MYSQL_HOST
from Bearcat_ProxyPool.settings import MYSQL_CHARSET
from Bearcat_ProxyPool.settings import MYSQL_PASSWORD

db = MySQLDatabase(MYSQL_DB, user=MYSQL_USER, host=MYSQL_HOST, port=MYSQL_PORT, password=MYSQL_PASSWORD,
                   charset=MYSQL_CHARSET)


class Proxies(Model):
    proxies = CharField(max_length=32)

    class Meta:
        database = db


class authenticated(Model):
    proxies = CharField(max_length=32)

    class Meta:
        database = db


# class BearcatProxypoolPipeline:
#     def process_item(self, item, spider):
#         return item
class SqlitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('proxies.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS proxies (proxies)")

    def process_item(self, item, spider):
        proxies = item.get('proxies')
        data = self.c.execute(f'SELECT proxies FROM proxies WHERE proxies="{proxies}"')
        self.conn.commit()
        if not list(data):
            self.c.execute(f"INSERT INTO proxies VALUES ('{proxies}')")
            self.conn.commit()
            logger.success(f'代理: {proxies}入数据库成功')
        else:
            logger.debug(f'数据库已有代理: {proxies}')
        return item

    def close_spider(self, spider):
        self.conn.close()


class RedisPipeline:
    def open_spider(self, spider):
        self.conn = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                         decode_responses=True,
                                         max_connections=REDIS_MAXCONNECTIONS,
                                         socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
        self.c = redis.Redis(connection_pool=self.conn)

    def process_item(self, item, spider):
        proxies = item.get('proxies')
        self.c.sadd('proxies', proxies)
        logger.success(f'代理: {proxies}入数据库成功')
        return item

    def close_spider(self, spider):
        self.conn.disconnect()


class MysqlPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                    charset=MYSQL_CHARSET)
        self.c = self.conn.cursor()
        self.c.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
        self.c.close()
        self.conn.close()
        Proxies.create_table()
        authenticated.create_table()

    def process_item(self, item, spider):
        proxies = item.get('proxies')
        try:
            Proxies.get(Proxies.proxies == proxies)
            logger.debug(f'数据库已有代理: {proxies}')
        except:
            Proxies(proxies=proxies).save()
            logger.success(f'代理: {proxies}入数据库成功')
        return item

    def close_spider(self, spider):
        pass
