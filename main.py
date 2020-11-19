import os
import sys

RASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(RASE_DIR)
import time
import threading
from verify import Verify
from scrapy import cmdline
from multiprocessing import Process
from Bearcat_ProxyPool.settings import SPIDER_TIME

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def start_blspider(spider_name, frequency):
    args = ['scrapy', 'crawl', spider_name]
    while True:
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        time.sleep(frequency)


if __name__ == '__main__':
    confs = [{"spider_name": "xici", "frequency": SPIDER_TIME},
             {"spider_name": "xila", "frequency": SPIDER_TIME},
             {"spider_name": "ihuan", "frequency": SPIDER_TIME},
             {"spider_name": "ip3366", "frequency": SPIDER_TIME},
             {"spider_name": "nima", "frequency": SPIDER_TIME},
             {"spider_name": "kuai", "frequency": SPIDER_TIME}]

    for conf in confs:
        process = Process(target=start_blspider, args=(conf.get("spider_name"), conf.get("frequency", 0)))
        process.start()
    proces = threading.Thread(target=Verify().main())
    proces.start()
