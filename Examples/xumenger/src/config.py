# -*- coding: utf-8 -*-

#多线程 or 多进程
isMultiProcess = False

#下载线程/进程个数
downloaderCount = 1

#解析线程/进程个数
parserCount = 1

#数据输出进程/线程个数
outputerCount = 1

#匹配的URL正则表达式，以及对应的处理类
urlREs = {'http://www.xumenger.com/.*/': 'xumenger', 
          'http://www.xumenger.com/page.*': 'page'}

#开始爬取的URL，支持配置以同时开始抓取多个网站
startURLs = ['http://www.xumenger.com', ]

#忽略不处理的URL
exceptURLs = ['http://www.xumenger.com/tags.*',
              'http://www.xumenger.com/categories.*',
              'http://www.xumenger.com/download/.*',
              'http://www.xumenger.com/media/.*']