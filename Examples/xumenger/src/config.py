# -*- coding: utf-8 -*-

#多线程 or 多进程
isMultiProcess = False

#下载线程/进程个数
downloadCount = 1

#解析线程/进程个数
parseCount = 1

#数据输出进程/线程个数
outputCount = 1

#匹配的URL正则表达式，以及对应的处理类的类名
reURLs = {'http://www.xumenger.com/.*/': 'xumenger', 
          'http://www.xumenger.com/page.*': 'page'}

#开始爬取的URL，支持配置多个URL，可用于同时抓取多个网站
startURLs = ['http://www.xumenger.com', ]

#忽略不处理的URL
exceptURLs = ['http://www.xumenger.com/tags.*',
              'http://www.xumenger.com/categories.*']

