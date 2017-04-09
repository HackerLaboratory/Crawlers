# -*- coding: utf-8 -*-

import os
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

class Crawler(object):
    """crawler class
        1. down html according to url
        2. parse html to get urls and content
        3. manage urls which are dealed and not dealed
        4. output content
    """

    def __init__(self, glbl):
        """crawler constructor
            1. register signal to control crawler suspend、resume、stop
            2. init downloader、parser、urlmanager、monitor
            3. use list to manage downloader、parser、urlmanager、outputer、monitor
            4. init lock to control multi thread or process
            5. use Queue to transmit urls and htmls between threads/processes and threads/processes
        """
        self.glbl = glbl
        self.isSuspend = False
        self.isStop = False
        # register signal
        signal.signal(signal.SIGINT, self.suspendResume)
        signal.signal(signal.SIGTSTP, self.stop)
        # init downloader、parser、urlmanager object
        self.downloader = dl.Downloader()
        self.parser = ps.Parser(cfg.urlREs, cfg.exceptUrlREs)
        self.urlmanager = um.UrlManager()
        # init lists to manage downloader、parser、urlmanager、outputer、monitor
        self.downloaderList = []
        self.parserList = []
        self.outputerList = []
        self.urlmanagerList = []
        self.monitorList = []
        # thread or process
        if cfg.isMultiProcess:
            self.Concurrency = multiprocessing.Process
            self.Lock = multiprocessing.Lock
            self.Queue = multiprocessing.Queue
        else:
            self.Concurrency = threading.Thread
            self.Lock = threading.Lock
            self.Queue = Queue.Queue
        # Queue and Lock
        self.inUrlQueue = self.Queue()
        self.outUrlQueue = self.Queue()
        self.htmlQueue = self.Queue()
        self.contentQueue = self.Queue()
        # init start urls
        for url in cfg.startUrls:
            self.inUrlQueue.put(url)
    

    def suspendResume(self, signum, frame):
        """suspend or resume crawler
        according to Ctrl-C signal
        """
        if self.isSuspend:
            print os.getpid(), ' get Ctrl-C signal to resume crawler'
        if not self.isSuspend:
            print os.getpid(), ' get Ctrl-C signal to suspend crawler'
        self.isSuspend = not self.isSuspend


    def stop(self, signum, frame):
        """stop crawler
        according to Ctrl-Z signal
        """
        print os.getpid(), ' get Ctrl-Z signal to stop crawler'
        self.isStop = True

    
    def run(self):
        """start crawler
        """
        self.Execute()

    
    def Execute(self):
        """start crawler
            1. start downloader
            2. start parser
            3. start outputer
            4. start urlmanager
            5. start monitor
        downloader、parser、outputer、urlmanager can config as thread or process
        monitor is crawler's main thread
        """
        for i in range(cfg.downloaderCount):
            concurrency = self.Concurrency(target = self.download)
            self.downloaderList.append(concurrency)
            concurrency.start()
        for i in range(cfg.parserCount):
            concurrency = self.Concurrency(target = self.parse)
            self.parserList.append(concurrency)
            concurrency.start()
        for i in range(cfg.outputerCount):
            concurrency = self.Concurrency(target = self.output)
            self.outputerList.append(concurrency)
            concurrency.start()
        for i in range(1):
            thread = threading.Thread(target = self.urlmanage)
            self.urlmanagerList.append(thread)
            thread.start()
        self.monitor()

    
    def monitor(self):
        """monitor is crawler's main thread
            1. monitor is used to moitor downloader、parser、outputer、urlmanager
            2. monitor is used to get Ctrl-C、Ctrl-Z signal
        """
        while not self.isStop:
            time.sleep(1)
        print 'monitor stop !'


    def urlmanage(self):
        """urlmanager run function
        """
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
        print 'urlmanager stop !'


    def download(self):
        """downloader run function
        """
        while not self.isStop:
            try:
                try:
                    url = self.outUrlQueue.get(False)
                except Queue.Empty as e:
                    continue
                if url is not None:
                    html = self.downloader.download(url, cfg.downloadTimeout)
                    if html is not None:
                        urlHtml = [url, html]
                        self.htmlQueue.put(urlHtml)
            except Exception as e:
                print "download error: ", e.message
        print 'downloader stop !'


    def parse(self):
        """ parser run function
        """
        while not self.isStop:
            try:
                try:
                    urlHtml = self.htmlQueue.get(False)
                except Queue.Empty as e:
                    time.sleep(1)
                    continue
                url = urlHtml[0]
                html = urlHtml[1]
                # parse HTML to get URL
                new_urls = self.parser.parseURL(urlHtml)
                if (new_urls is not None) and (0 < len(new_urls)):
                    for new_url in new_urls:
                        self.inUrlQueue.put(new_url)
                # get deal class according to url, then call parse function
                for k in cfg.urlREs.keys():
                    pattern = re.compile(k)
                    if pattern.match(url):
                        # find deal class according to url
                        dealURL = self.glbl[cfg.urlREs[k]]
                        dealurl = dealURL()
                        content = dealurl.Parse(html)
                        if content is not None:
                            urlContent = [url, content]
                            self.contentQueue.put(urlContent)
            except Exception as e:
                print "parse error: ", e.message
        print 'parser stop !'


    def output(self):
        """outputer run function
        """
        while not self.isStop:
            try:
                try:
                    urlContent = self.contentQueue.get(False)
                except Queue.Empty as e:
                    time.sleep(1)
                    continue
                url = urlContent[0]
                content = urlContent[1]
                # get deal class according to url, then call output function
                for k in cfg.urlREs.keys():
                    pattern = re.compile(k)
                    if pattern.match(url):
                        # find deal class according to url
                        dealURL = self.glbl[cfg.urlREs[k]]
                        dealurl = dealURL()
                        dealurl.Output(content)
            except Exception as e:
                print "output error: ", e.message
        print 'outputer stop !'

