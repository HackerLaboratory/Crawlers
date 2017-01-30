# -*- coding: utf-8 -*-
"""
实现一个爬虫框架
* 实现基础的下载器、url管理器、解析器、输出器方法
* 开发者可以重载这四个方法，个性化自己的爬虫
"""

# 引入基础包
import multiprocessing
import threading
import re
import urllib
import urllib2

# 导入配置文件中的配置信息
from config import isMultiProcess
from config import downloadCount
from config import outputCount
from config import reURLs
from config import startURL

class Crawler(object):
    def __init__(self):
        print 'init'

    # URL下载方法
    def download(self):
        print 'download'

    # URL管理方法
    def manage(self):
        print 'manage'

    # HTML解析方法
    def parse(self):
        print 'parse'

    # 解析内容输出(存储方法)
    def output(self):
        print 'output'

    # 按照配置的线程/进程、按照实现的方法运行爬虫
    def Execute(self):
        if isMultiProcess:
            MultiKind = multiprocessing.Process
        else:
            MultiKind = threading.Thread

        # 按照配置启动n个下载线程/进程
        for i in range(downloadCount):
            multi = MultiKind(target=self.download)
            multi.start()

        # 按照配置启动n个输出线程/进程
        for i in range(outputCount):
            multi = MultiKind(target=self.output)
            multi.start()

