# -*- coding: utf-8 -*-

#多线程 or 多进程
isMultiProcess = True

#下载器线程/进程个数
downloadCount = 2

#数据存储器进程/线程个数
outputCount = 2

#匹配的URL正则表达式
reURLs = {'url1': ['download1', 'output1'], 
          'url2': ['download2', 'output2']}

#开始爬取的URL
startURL = 'http://www.xumenger.com'
