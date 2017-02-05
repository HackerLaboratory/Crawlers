# -*- coding: utf-8 -*-

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
实现一个爬虫框架
* 实现基础的下载器、url管理器、解析器、输出器方法
* 开发者可以重载这相关方法，个性化自己的爬虫

有以下三种线程/进程
* 下载：下载html页面，放到htmlQueue中
* 解析：从htmlQueue中取出html页面进行解析，解析的URL放入URL管理器，解析的内容放到parseQueue
* 输出：从parseQueue中取出解析得到的内容，输出（或者文件，或者数据库，或者其他）
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# 引入基础包
import multiprocessing
import threading
import Queue
import logging
import time
import re
import urllib
import urllib2
import urlparse


# 导入配置文件中的配置信息
from config import isMultiProcess
from config import downloadCount
from config import parseCount
from config import outputCount
from config import reURLs
from config import startURL


# 爬虫基类
class Crawler(object):

    def __init__(self):
        self.isClose = False
        #日志配置
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log',
                filemode='w')
        #初始化url管理器(集合)
        self.new_urls = set()       #新的还未被爬取的url集合，使用集合进行管理
        self.old_urls = set()       #已经被爬取过的url集合，也是使用集合进行管理
        self.new_urls.add(startURL) #将初始化URL放到new_urls中
        #多线程/多进程管理列表
        self.downLoadList = []      #下载线程/进程链表
        self.parseList = []         #解析线程/进程链表
        self.outputList = []        #输出线程/进程链表
        #配置多线程 or 多进程
        if isMultiProcess:
            self.multiKind = multiprocessing.Process
            self.multiLock = multiprocessing.Lock()
            self.htmlQueue = multiprocessing.Queue()
            self.parseQueue = multiprocessing.Queue()
        else:
            self.multiKind = threading.Thread
            self.multiLock = threading.Lock()
            self.htmlQueue = Queue.Queue()
            self.parseQueue = Queue.Queue()


    """""""""""""""""""""""""""""""""""""""""
    URL下载相关方法
    """""""""""""""""""""""""""""""""""""""""
    # URL下载线程/进程方法
    def download(self):
        while not self.isClose:
            try:
                ErrCode = 0
                url = self.get_new_url()
                ErrCode = 1
                if url is None:
                    ErrCode = 2
                    time.sleep(1)
                    ErrCode = 3
                    continue
                ErrCode = 4
                #使用urllib2下载url指向的html内容
                response = urllib2.urlopen(url)
                ErrCode = 5
                #如果http的返回码不是200，说明请求下载失败
                if 200 == response.getcode():
                    ErrCode = 6
                    pageHtml = response.read()
                    #下载到的htlm字符串放入htmlQueue队列
                    ErrCode = 7
                    html = [url, pageHtml]
                    self.htmlQueue.put(html)
                    ErrCode = 8
            except Exception, e:
                logging.error('下载网页出现异常，ErrCode=' + str(ErrCode) + ', 异常信息: ' + e.message)

                
    """""""""""""""""""""""""""""""""""""""""
    URL管理器相关方法
    """""""""""""""""""""""""""""""""""""""""
    # 添加一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        self.multiLock.acquire()
        try:
            if (url not in self.new_urls) and (url not in self.old_urls):
                self.new_urls.add(url)
        finally:
            self.multiLock.release()

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
        self.multiLock.acquire()
        try:
            if 0 < len(self.new_urls):
                #pop方法时从集合中获取一个元素，并将其从集合中移除
                new_url = self.new_urls.pop()
                self.old_urls.add(new_url)
                return new_url
            else:
                return None
        finally:
            self.multiLock.release()


    """""""""""""""""""""""""""""""""""""""""
    HTML解析相关方法
    """""""""""""""""""""""""""""""""""""""""
    # 解析HTML获取其中的URL
    def parseURL(self, html):
        new_urls = []
        url = html[0]
        pageHtml = html[1]
        #使用正则表达式获取网页中所有的URL链接
        pattern = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        urls = pattern.findall(pageHtml)
        for u in urls:
            #拼接成完整的URL
            new_full_url = urlparse.urljoin(url, u)
            #判断该URL是否符合在config.py中的reURLs配置
            for k in reURLs.keys():
                pattern = re.compile(k)
                if pattern.match(new_full_url) is not None:
                    print new_full_url
                    new_urls.append(new_full_url)
        return new_urls

    # 解析HTML获取想要的内容
    def parseContent(self, html):
        #基类中给出最简单的解析方法(不解析)
        url = html[0]
        pageHtml = html[1]
        return [pageHtml] 

    # HTML解析线程/进程方法
    def parse(self):
        while not self.isClose:
            try:
                ErrCode = 0
                html = self.htmlQueue.get(False)
                ErrCode = 1
                #将新的url放入url管理器
                urls = self.parseURL(html)
                ErrCode = 2
                self.add_new_urls(urls)
                ErrCode = 3
                #将解析的内容放入parseQueue
                content = self.parseContent(html)
                ErrCode = 4
                if content is not None:
                    ErrCode = 5
                    self.parseQueue.put(content)
                    ErrCode = 6
            except Queue.Empty, e:
                logging.error('htmlQueue中暂时没有数据')
                time.sleep(1)
            except Exception, e:
                logging.error('解析网页出现异常, ErrCode=' + str(ErrCode) + ', 异常信息: ' + e.message)
                time.sleep(1)
            else:
                logging.error('解析网页出现其他异常')
                time.sleep(1)


    """""""""""""""""""""""""""""""""""""""""
    解析内容输出相关方法
    """""""""""""""""""""""""""""""""""""""""
    # 输出内容
    def outputContent(self, content):
        #基类中给出默认的输出方法(不输出)
        pass

    # 解析内容输出(存储方法)
    def output(self):
        while not self.isClose:
            try:
                ErrCode = 0
                content = self.parseQueue.get(False)
                ErrCode = 1
                self.outputContent(content)
                ErrCode = 2
            except Queue.Empty, e:
                logging.error('parseQueue中暂时没有数据')
                time.sleep(1)
            except Exception, e:
                logging.error('输出内容出现异常, ErrCode=' + str(ErrCode) + ', 异常信息: ' + e.message)
                time.sleep(1)
            else:
                logging.error('输出内容出现其他异常')
                time.sleep(1)


    """""""""""""""""""""""""""""""""""""""""
    爬虫运行方法
    """""""""""""""""""""""""""""""""""""""""
    # 按照配置的线程/进程、按照实现的方法运行爬虫
    def Execute(self):
        #按照配置启动n个下载线程/进程
        for i in range(downloadCount):
            multi = self.multiKind(target=self.download)
            self.downLoadList.append(multi)
            multi.start()

        #按照配置启动n个解析线程/进程
        for i in range(parseCount):
            multi = self.multiKind(target=self.parse)
            self.parseList.append(multi)
            multi.start()

        #按照配置启动n个输出线程/进程
        for i in range(outputCount):
            multi = self.multiKind(target=self.output)
            self.outputList.append(multi)
            multi.start()

