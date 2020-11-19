import os
import sys
import redis
import random
import pymysql
import sqlite3
from flask import Flask
from Bearcat_ProxyPool.settings import REDIS_DB
from Bearcat_ProxyPool.settings import DATABASE
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

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return '请访问/authenticated获取代理'


@app.route('/authenticated', methods=['GET'])
def authenticated():
    if DATABASE == 'sqlite':
        conn = sqlite3.connect('proxies.db')
        c = conn.cursor()
        proxies_list = [i[0] for i in c.execute('SELECT proxies FROM authenticated')]
        proxies = random.choice(proxies_list)
    elif DATABASE == 'redis':
        conn = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                    decode_responses=True,
                                    max_connections=REDIS_MAXCONNECTIONS,
                                    socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
        c = redis.Redis(connection_pool=conn)
        proxies = c.srandmember('authenticated')
    elif DATABASE == 'mysql':
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                               charset=MYSQL_CHARSET, db=MYSQL_DB)
        c = conn.cursor()
        c.execute(f'SELECT proxies FROM authenticated')
        proxies = random.choice([i[0] for i in c.fetchall()])
    else:
        proxies = None
    return proxies


@app.route('/count', methods=['GET'])
def count():
    if DATABASE == 'sqlite':
        conn = sqlite3.connect('proxies.db')
        c = conn.cursor()
        proxies = len(list(c.execute('SELECT proxies FROM authenticated')))
    elif DATABASE == 'redis':
        conn = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                    decode_responses=True,
                                    max_connections=REDIS_MAXCONNECTIONS,
                                    socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
        c = redis.Redis(connection_pool=conn)
        proxies = len(list(c.smembers('authenticated')))
    elif DATABASE == 'mysql':
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                               charset=MYSQL_CHARSET, db=MYSQL_DB)
        c = conn.cursor()
        c.execute(f'SELECT proxies FROM authenticated')
        proxies = len([i[0] for i in c.fetchall()])
    else:
        proxies = None
    return f'可用IP数量为: {proxies}'


@app.route('/all', methods=['GET'])
def all():
    if DATABASE == 'sqlite':
        conn = sqlite3.connect('proxies.db')
        c = conn.cursor()
        proxies = list(c.execute('SELECT proxies FROM authenticated'))
    elif DATABASE == 'redis':
        conn = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PARAMS,
                                    decode_responses=True,
                                    max_connections=REDIS_MAXCONNECTIONS,
                                    socket_connect_timeout=REDIS_CONNECT_TIMEOUT)
        c = redis.Redis(connection_pool=conn)
        proxies = list(c.smembers('authenticated'))
    elif DATABASE == 'mysql':
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                               charset=MYSQL_CHARSET, db=MYSQL_DB)
        c = conn.cursor()
        c.execute(f'SELECT proxies FROM authenticated')
        proxies = [i[0] for i in c.fetchall()]
    else:
        proxies = None
    return f'可用IP为: {proxies}'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
