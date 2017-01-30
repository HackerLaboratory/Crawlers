# -*- coding: utf-8 -*-
"""
实现一个爬虫框架
* 实现基础的下载器、url管理器、解析器、输出器方法
* 开发者可以重载这四个方法，个性化自己的爬虫
"""

# 引入基础包
import multiprocessing
import threading
import Queue
import time
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
        # 初始化url管理器(集合)
        self.new_urls = set()       #新的还未被爬取的url集合，使用集合进行管理
        self.old_urls = set()       #已经被爬取过的url集合，也是使用集合进行管理
        # 初始化html输出队列
        htmlQueue = Queue.Queue()   #下载下来的html页面存放的队列
        parseQueue = Queue.Queue()  #解析后内容存储的队列
        # 配置多线程 or 多进程
        if isMultiProcess:
            self.MultiKind = multiprocessing.Process
            self.MultiLock = multiprocessing.Lock()
        else:
            self.MultiKind = threading.Thread
            self.MultiLock = threading.Lock()

    """
    URL下载相关方法
    """
    # URL下载方法
    def download(self):
        while True:
            try:
                url = self.get_new_url()
                if url is None:
                    time.sleep(10)
                # 使用urllib2下载url指向的html内容
                response = urllib2.urlopen(url)
                # 如果http的返回码不是200，说明请求下载失败
                if 200 == response.getcode():
                    html = response.read()
                    htmlQueue.put(html)
            except Exception, e:
                print Exception, ': ', e

                
    """
    URL管理器相关方法
    """
    # 添加一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        if (url not in self.new_urls) and (url not in self.old_urls):
            self.MultiLock.acquire()
            try:
                self.new_urls.add(url)
            finally:
                self.MultiLock.release()

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
        self.MultiLock.acquire()
        try:
            new_url = self.new_urls.pop()   #pop方法是从集合中获取一个元素，并将其中集合中移除
            self.old_urls.add(new_url)
            return new_url
        finally:
            self.MultiLock.release()

    """
    HTML解析相关方法
    """
    # HTML解析方法
    def parse(self):
        print 'parse'

    """
    解析内容输出相关方法
    """
    # 解析内容输出(存储方法)
    def output(self):
        print 'output'

    """
    爬虫运行方法
    """
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

