# -*- coding: utf-8 -*-

#多线程 or 多进程
isMultiProcess = False

#下载线程/进程个数
downloadCount = 3

#解析线程/进程个数
parseCount = 2

#数据存储进程/线程个数
outputCount = 3

#匹配的URL正则表达式
reURLs = {'http://www.xumenger.com/.*/': 'xumenger', 
          'http://www.xumenger.com/page.*': 'page'}

#开始爬取的URL
startURLs = ['http://www.xumenger.com']

