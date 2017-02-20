# -*- coding: utf-8 -*-

import multiprocessing
import threading
import Queue
import time
import re

import config as cfg
import downloader as dl
import parser as ps
import urlmanager as um

"""爬虫类
异常处理需要完善
* 网络异常
* 配置的url处理类异常
* 解析异常
* 存储异常

逻辑完善
* 线程/进程合理退出
* 进程间数据传递
"""
class Crawler(object):

    def __init__(self, glbl):
        self.glbl = glbl
        self.isClose = False

        self.downloader = dl.Downloader()
        self.parser = ps.Parser(cfg.reURLs)
        self.urlmanager = um.UrlManager()
        
        self.downloaderList = []
        self.parserList = []
        self.outputerList = []
        self.urlmanagerList = []
        
        if cfg.isMultiProcess:
            self.Concurrency = multiprocessing.Process
            self.Lock = multiprocessing.Lock
            self.Queue = multiprocessing.Queue
        else:
            self.Concurrency = threading.Thread
            self.Lock = threading.Lock
            self.Queue = Queue.Queue

        self.inUrlQueue = self.Queue()
        self.outUrlQueue = self.Queue()
        self.htmlQueue = self.Queue()
        self.contentQueue = self.Queue()
        self.inUrlQueue.put(cfg.startURL)

    
    def run(self):
        self.Execute()

    
    def Execute(self):
        for i in range(cfg.downloadCount):
            concurrency = self.Concurrency(target = self.download)
            self.downloaderList.append(concurrency)
            concurrency.start()
        for i in range(cfg.parseCount):
            concurrency = self.Concurrency(target = self.parse)
            self.parserList.append(concurrency)
            concurrency.start()
        for i in range(cfg.outputCount):
            concurrency = self.Concurrency(target = self.output)
            self.outputerList.append(concurrency)
            concurrency.start()
        for i in range(1):
            concurrency = threading.Thread(target = self.urlmanage)
            self.urlmanagerList.append(concurrency)
            concurrency.start()


    def urlmanage(self):
        while not self.isClose:
            outUrl = self.urlmanager.get_new_url()
            if outUrl is not None:
                self.outUrlQueue.put(outUrl)
            try:
                inUrl = self.inUrlQueue.get(False)
            except Queue.Empty as e:
                time.sleep(1)
                continue
            self.urlmanager.add_new_url(inUrl)


    def download(self):
        while not self.isClose:
            try:
                try:
                    url = self.outUrlQueue.get(False)
                except Queue.Empty as e:
                    continue
                if url is not None:
                    html = self.downloader.download(url)
                    urlHtml = [url, html]
                    self.htmlQueue.put(urlHtml)
            except Exception as e:
                print "download error: ", e.message


    def parse(self):
        while not self.isClose:
            try:
                try:
                    urlHtml = self.htmlQueue.get(False)
                except Queue.Empty as e:
                    time.sleep(1)
                    continue
                url = urlHtml[0]
                html = urlHtml[1]
                #解析HTML获取URL
                new_urls = self.parser.parseURL(urlHtml)
                if (new_urls is not None) and (0 < len(new_urls)):
                    for new_url in new_urls:
                        self.inUrlQueue.put(new_url)
                #根据URL找到对应的处理类，然后调用解析方法
                for k in cfg.reURLs.keys():
                    pattern = re.compile(k)
                    if pattern.match(url):
                        #找到对应的URL处理类
                        dealURL = self.glbl[cfg.reURLs[k]]
                        dealurl = dealURL()
                        content = dealurl.Parse(html)
                        if content is not None:
                            urlContent = [url, content]
                            contentQueue.put(urlContent)
            except Exception as e:
                print "parse error: ", e.message


    def output(self):
        while not self.isClose:
            try:
                try:
                    urlContent = self.contentQueue.get(False)
                except Queue.Empty as e:
                    time.sleep(1)
                    continue
                url = urlContent[0]
                content = urlContent[1]
                #根据URL找到对应的处理类，然后调用输出方法
                for k in cfg.reURLs.keys():
                    pattern = re.compile(k)
                    if pattern.match(url):
                        #找到对应的URL处理类
                        dealURL = self.glbl[cfg.reURLs[k]]
                        dealurl = dealURL()
                        dealurl.Output(content)
            except Exception as e:
                print "output error: ", e.message


