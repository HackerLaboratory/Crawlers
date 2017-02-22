# -*- coding: utf-8 -*-

import crawler
import re
import threading
import time
import matplotlib.pyplot as plt

craw = crawler.Crawler(globals())
lock = threading.Lock()
result = {}

#要求实现的url处理类必须是并发安全的！

#xumenger类用来解析获取每篇文章的tag
class xumenger(object):    
    def __init__(self):
        self.pattern = re.compile(r'<a href="/tags/#(.*?)" title=.*?>')

    def Parse(self, html):
        content = []
        tags = self.pattern.findall(html, re.S|re.M)
        if tags is not None:
            for tag in tags:
                content.append(tag)
        return content

    def Output(self, content):
        global lock
        global result
        for tag in content:
            lock.acquire()
            try:
                tag = tag.lower()
                if tag in result.keys():
                    result[tag] = result[tag] + 1
                else:
                    result[tag] = 1
            finally:
                lock.release()

#page类不做解析，只是为了遍历所有URL
class page(object):
    def Parse(self, html):
        return None

    def Output(self, content):
        pass


if __name__ == '__main__':
    craw.run()
    
    times = 1800
    while times > 0:
        time.sleep(1)
        times = times - 1

    lock.acquire()
    try:
        #按值对字典排序
        sort = sorted(result.iteritems(), key=lambda d:d[1], reverse=True)
        tagsort = []
        for i in range(10):
            tagsort.append(sort[i])     
    finally:
        lock.release()
   
    for tag in tagsort:
        print tag[0], ':', tag[1]
