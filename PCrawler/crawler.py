# -*- coding: utf-8 -*-

# 引入基础包
import multiprocessing
import threading
import re

# 导入配置文件中的配置信息
from config import isMultiProcess
from config import downloader
from config import outputer
from config import reURL
from config import startURL

class Crawler(object):

    # URL下载方法
    def download():
        pass

    # URL管理方法
    def manage():
        pass

    # HTML解析方法
    def parse():
        pass

    # 解析内容输出(存储方法)
    def output():
        pass

    # 按照配置的线程/进程、按照实现的方法运行爬虫
    def Execute():
        pass
        # 按照配置启动n个下载线程/进程

        # 按照配置启动n个输出线程/进程

