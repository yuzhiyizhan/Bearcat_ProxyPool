# Scrapy settings for Bearcat_ProxyPool project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Bearcat_ProxyPool'

SPIDER_MODULES = ['Bearcat_ProxyPool.spiders']
NEWSPIDER_MODULE = 'Bearcat_ProxyPool.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Bearcat_ProxyPool (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
# DOWNLOAD_TIMEOUT = 5
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
DOWNLOAD_WARNSIZE = 0
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Bearcat_ProxyPool.middlewares.BearcatProxypoolSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'Bearcat_ProxyPool.middlewares.BearcatProxypoolDownloaderMiddleware': 543,
    'Bearcat_ProxyPool.middlewares.UserAgentDownloadMiddleware': 1,
    'Bearcat_ProxyPool.middlewares.LogDownloadMiddleware': 2,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 选择数据库
DATABASE = 'sqlite'
if DATABASE == 'sqlite':
    ITEM_PIPELINES = {
        'Bearcat_ProxyPool.pipelines.SqlitePipeline': 1
    }
elif DATABASE == 'redis':
    ITEM_PIPELINES = {
        'Bearcat_ProxyPool.pipelines.RedisPipeline': 2
    }
elif DATABASE == 'mysql':
    ITEM_PIPELINES = {
        'Bearcat_ProxyPool.pipelines.MysqlPipeline': 3
    }
else:
    raise ValueError('请指定数据库,如果来不及安装可以设置为: Sqlite')

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# # The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 代理类型（填HTTP或HTTPS）
PROXIES_MODE = 'HTTPS'
# 爬取目标网站
VERIFICATION_URL = 'https://www.mzitu.com/japan/'
# 爬取目标使用的请求头
VERIFICATION_HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'referer': 'https://www.mzitu.com/japan/',
}

# redis服务配置
# redis主机名
REDIS_HOST = '127.0.0.1'
# redis端口
REDIS_PORT = '6379'
# redis密码
REDIS_PARAMS = ''
# redis db
REDIS_DB = 1
# redis最大连接数
REDIS_MAXCONNECTIONS = 100
# redis超时时间
REDIS_CONNECT_TIMEOUT = 30

# mysql服务配置
# mysql主机名
MYSQL_HOST = 'localhost'
# mysql用户名
MYSQL_USER = 'liang'
# mysql密码
MYSQL_PASSWORD = '123456'
# mysql端口
MYSQL_PORT = 3306
# mysql db
MYSQL_DB = 'PROXIES'
# 编码
MYSQL_CHARSET = 'utf8mb4'
# 验证模块等待多长时间验证全部代理活性
VERIFY_TIME = 180
# 验证代理线程数(越大越快,资源占用也越多)
MAX_WORKERS = 50
# 爬虫等待多长时间启动一次
SPIDER_TIME = 30
