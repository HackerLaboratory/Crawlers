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

# 爬虫基类
class Crawler(object):

    def __init__(self):
        print 'init'
        # 初始化url管理器(集合)
        self.new_urls = set()       #新的还未被爬取的url集合，使用集合进行管理
        self.old_urls = set()       #已经被爬取过的url集合，也是使用集合进行管理
        # 配置多线程 or 多进程
        if isMultiProcess:
            self.MultiKind = multiprocessing.Process
        else:
            self.MultiKind = threading.Thread

    # URL下载方法
    def download(self):
        print 'download'

    # 添加一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        if (url not in self.new_urls) and (url not in self.old_urls):
            self.new_urls.add(url)
    # 添加批量url
    def add_new_urls(self, urls):
        if (urls is None) or (0 == len(urls)):
            return
        for url in urls:
            self.add_new_url(url)
    # 判断是否还有未爬取的url
    def has_new_url(self):
        return (0 != len(self.new_urls))
    # 获取一个新的待爬取的url
    def get_new_url(self):
        new_url = self.new_urls.pop()   #pop方法是从集合中获取一个元素，并将其中集合中移除
        self.old_urls.add(new_url)
        return new_url

    # HTML解析方法
    def parse(self):
        print 'parse'

    # 解析内容输出(存储方法)
    def output(self):
        print 'output'

    # 按照配置的线程/进程、按照实现的方法运行爬虫
    def Execute(self):
        # 按照配置启动n个下载线程/进程
        for i in range(downloadCount):
            multi = self.MultiKind(target=self.download)
            multi.start()

        # 按照配置启动n个输出线程/进程
        for i in range(outputCount):
            multi = self.MultiKind(target=self.output)
            multi.start()

