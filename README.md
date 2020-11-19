# 熊猫代理池

1.先进行配置: 到BearCat_ProxyPool.settings.py设置如下:


	爬取目标网站(验证的网站)

	## 代理类型（填HTTP或HTTPS）
	PROXIES_MODE = 'HTTPS'

	## 爬取目标网站
	VERIFICATION_URL = 'https://www.mzitu.com/japan/'

	## 爬取目标使用的请求头
	VERIFICATION_HEADERS = {
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
		'referer': 'https://www.mzitu.com/japan/',
	}

	## redis服务配置
	# redis主机名
	REDIS_HOST = '127.0.0.1'

	## redis端口
	REDIS_PORT = '6379'

	## redis密码
	REDIS_PARAMS = ''

	## redis db
	REDIS_DB = 1
	## redis最大连接数
	REDIS_MAXCONNECTIONS = 100

	## redis超时时间
	REDIS_CONNECT_TIMEOUT = 30


	## mysql服务配置
	# mysql主机名
	MYSQL_HOST = 'localhost'

	## mysql用户名
	MYSQL_USER = 'liang'

	## mysql密码
	MYSQL_PASSWORD = '123456'

	## mysql端口
	MYSQL_PORT = 3306

	## mysql db
	MYSQL_DB = 'PROXIES'

	## 编码
	MYSQL_CHARSET = 'utf8mb4'

	## 验证模块等待多长时间验证全部代理活性
	VERIFY_TIME = 180

	## 验证代理线程数(越大越快,资源占用也越多)
	MAX_WORKERS = 50

	## 爬虫等待多长时间启动一次
	SPIDER_TIME = 30

	## 选择数据库(如果没有数据库，可以先用sqlite先用着)
	DATABASE = 'sqlite'
	​
	其他设置看scrapy文档,我打开了智能等待做个友好的爬虫人

2.安装依赖:

	cd 到项目目录Bearcat_ProxyPool

	pip3 install -r requirements.txt -i https://pypi.douban.com/simple/

	pip3 install --upgrade -r requirements.txt -i https://pypi.douban.com/simple/
	​
	3.安装数据库

	安装(linux)

	第一种:下载，解压，编译Redis

	$ wget http://download.redis.io/releases/redis-5.0.5.tar.gz

	$ tar xzf redis-5.0.5.tar.gz

	$ cd redis-5.0.5

	$ make

	进入到解压后的 src 目录，通过如下命令启动Redis：

	$ src/redis-server

	您可以使用内置的客户端与Redis进行互动：

	$ src/redis-cli

	第二种:
	ubuntu
	sudo apt-get install redis
	redis-server

	manjaro
	sudo pacman -S redis
	redis-server

	windows

	下载地址
	https://github.com/microsoftarchive/redis/releases
	安装过程自行百度(其实就是解压后点redis-server)

	也可以用MYSQL连MYSQL也没有的话可以用sqlite

3.启动爬虫

	到相关路径下使用命令

	python main.py
	
	python app.py
	
4.查看代理

	启动项目后访问以下网址
	
	随机返回一个代理
	
	http://127.0.0.1:5555/authenticated
	
	可用代理总数
	
	http://127.0.0.1:5555/count
	
	返回全部代理
	
	http://127.0.0.1:5555/all

5.添加代理IP爬虫

	到项目路径下用scrapy的命令增加爬虫
	
	scrapy genspider example example.com
	
	yield一个代理IP给BearcatProxypoolItem
	
	yield BearcatProxypoolItem(proxies=proxies)
	
	到main文件将爬虫的名字增加到confs列表中
	
	{"spider_name": "example", "frequency": SPIDER_TIME}
