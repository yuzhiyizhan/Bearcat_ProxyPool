import os
import sys
import redis
import sqlite3
import pymysql
import requests
from loguru import logger
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from Bearcat_ProxyPool.settings import REDIS_DB
from Bearcat_ProxyPool.settings import DATABASE
from Bearcat_ProxyPool.settings import REDIS_HOST
from Bearcat_ProxyPool.settings import REDIS_PORT
from Bearcat_ProxyPool.settings import REDIS_PARAMS
from Bearcat_ProxyPool.settings import PROXIES_MODE
from Bearcat_ProxyPool.settings import VERIFICATION_URL
from Bearcat_ProxyPool.settings import VERIFICATION_HEADERS
from Bearcat_ProxyPool.settings import REDIS_MAXCONNECTIONS
from Bearcat_ProxyPool.settings import REDIS_CONNECT_TIMEOUT
from Bearcat_ProxyPool.settings import MYSQL_DB
from Bearcat_ProxyPool.settings import MYSQL_USER
from Bearcat_ProxyPool.settings import MYSQL_PORT
from Bearcat_ProxyPool.settings import MYSQL_HOST
from Bearcat_ProxyPool.settings import MYSQL_CHARSET
from Bearcat_ProxyPool.settings import MYSQL_PASSWORD
from Bearcat_ProxyPool.settings import MAX_WORKERS

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Verify(object):
    def __init__(self):
        self.DATABASE = DATABASE
        if self.DATABASE == 'sqlite':
            self.conn = sqlite3.connect('proxies.db')
            self.c = self.conn.cursor()
        elif self.DATABASE == 'redis':
            self.conn = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                             decode_responses=True,
                                             max_connections=REDIS_MAXCONNECTIONS,
                                             socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
            self.c = redis.Redis(connection_pool=self.conn)
        elif self.DATABASE == 'mysql':
            self.conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                        charset=MYSQL_CHARSET, db=MYSQL_DB)
            self.c = self.conn.cursor()
        else:
            self.conn = None
            self.c = None

    def get_proxies(self):
        if self.DATABASE == 'sqlite':
            return [i[0] for i in list(self.c.execute('SELECT proxies FROM proxies'))]
        elif self.DATABASE == 'redis':
            return list(self.c.smembers('proxies'))
        elif self.DATABASE == 'mysql':
            self.c.execute(f'SELECT proxies FROM proxies')
            return [i[0] for i in self.c.fetchall()]

    def success_verify_proxy(self, proxies):
        if self.DATABASE == 'sqlite':
            self.c.execute("CREATE TABLE IF NOT EXISTS authenticated (proxies)")
            data = self.c.execute(f'SELECT proxies FROM authenticated WHERE proxies="{proxies}"')
            self.conn.commit()
            if not list(data):
                self.c.execute(f"INSERT INTO authenticated VALUES ('{proxies}')")
                self.conn.commit()
                logger.success(f'代理: {proxies}入已验证代理数据库成功')
            else:
                logger.success(f'已验证代理数据库已有代理: {proxies}')
        elif self.DATABASE == 'redis':
            self.c.sadd('authenticated', proxies)
            logger.success(f'代理: {proxies}入已验证代理数据库成功')
        elif self.DATABASE == 'mysql':
            data = self.c.execute(f'SELECT proxies FROM authenticated WHERE proxies="{proxies}"')
            self.conn.commit()
            if data == 0:
                self.c.execute(f'INSERT INTO authenticated (proxies) VALUES ("{proxies}")')
                self.conn.commit()
                logger.success(f'代理: {proxies}入已验证代理数据库成功')
            else:
                logger.success(f'已验证代理数据库已有代理: {proxies}')

    def error_verify_proxy(self, proxies):
        if self.DATABASE == 'sqlite':
            self.c.execute("CREATE TABLE IF NOT EXISTS authenticated (proxies)")
            data = self.c.execute(f'SELECT proxies FROM authenticated WHERE proxies="{proxies}"')
            self.conn.commit()
            if not list(data):
                logger.error(f'已验证代理数据库已删除代理: {proxies}')
            else:
                self.c.execute(f'DELETE FROM authenticated WHERE proxies="{proxies}"')
                self.conn.commit()
                logger.error(f'已验证代理数据库已删除代理: {proxies}')
        elif self.DATABASE == 'redis':
            self.c.srem('authenticated', proxies)
            logger.error(f'已验证代理数据库已删除代理: {proxies}')
        elif self.DATABASE == 'mysql':
            data = self.c.execute(f'SELECT proxies FROM authenticated WHERE proxies="{proxies}"')
            self.conn.commit()
            if data != 0:
                self.c.execute(f'DELETE FROM authenticated WHERE proxies="{proxies}"')
                self.conn.commit()
                logger.error(f'已验证代理数据库已删除代理: {proxies}')
            else:
                logger.error(f'已验证代理数据库已删除代理: {proxies}')

    def verify(self, i):
        if PROXIES_MODE == 'HTTPS':
            proxies = {'https': 'https://' + i}
        else:
            proxies = {'http': 'http://' + i}
        error = 0
        while True:
            try:
                response = requests.get(url=VERIFICATION_URL, headers=VERIFICATION_HEADERS, proxies=proxies,
                                        timeout=3)
                if response.status_code == 200:
                    return {'success': i}
            except:
                error = error + 1
                if error > 3:
                    return {'error': i}
                else:
                    logger.debug(f'重试代理: {i} {error}次')
                    continue

    def main(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as t:
            obj_list = []
            for i in self.get_proxies():
                obj = t.submit(self.verify, i)
                obj_list.append(obj)
            for i in as_completed(obj_list):
                proxies = i.result()
                if proxies.get('success'):
                    self.success_verify_proxy(proxies.get('success'))
                else:
                    self.error_verify_proxy(proxies.get('error'))


if __name__ == '__main__':
    Verify().main()
