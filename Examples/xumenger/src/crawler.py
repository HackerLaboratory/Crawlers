# -*- coding: utf-8 -*-

import signal
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

暂停、恢复、停止的信息怎么发送给其他进程/线程
新增一个监控线程可以专门用于监控和控制其他线程/进程？
"""
class Crawler(object):

    def __init__(self, glbl):
        self.glbl = glbl
        self.isSuspend = False
        self.isStop = False

        #注册信号，通过信号来控制爬虫的暂停、恢复、停止
        signal.signal(signal.SIGINT, self.suspendResume)
        signal.signal(signal.SIGTSTP, self.stop)

        self.downloader = dl.Downloader()
        self.parser = ps.Parser(cfg.reURLs)
        self.urlmanager = um.UrlManager()
        
        self.downloaderList = []
        self.parserList = []
        self.outputerList = []
        self.urlmanagerList = []
        self.monitorList = []
        
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
        for url in cfg.startURLs:
            self.inUrlQueue.put(url)
    

    def suspendResume(self, signum, frame):
        print 'Ctrl-C suspend/resume'
        self.isSuspend = not self.isSuspend


    def stop(self, signum, frame):
        print 'Ctrl-Z stop'
        self.isStop = True

    
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
        for i in range(1):
            concurrency = threading.Thread(target = self.monitor)
            self.monitorList.append(concurrency)
            concurrency.start()

    
    def monitor(self):
        pass


    def urlmanage(self):
        while not self.isStop:
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
        while not self.isStop:
            try:
                try:
                    url = self.outUrlQueue.get(False)
                except Queue.Empty as e:
                    continue
                if url is not None:
                    html = self.downloader.download(url)
                    if html is not None:
                        urlHtml = [url, html]
                        self.htmlQueue.put(urlHtml)
            except Exception as e:
                print "download error: ", e.message


    def parse(self):
        while not self.isStop:
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
                            self.contentQueue.put(urlContent)
            except Exception as e:
                print "parse error: ", err, e.message


    def output(self):
        while not self.isStop:
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

