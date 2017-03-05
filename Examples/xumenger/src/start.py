# -*- coding: utf-8 -*-

import crawler
import re
import threading
import time
import matplotlib.pyplot as plt
import numpy as np

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


#需要控制，假如这里运行完成就相当于主进程的主线程运行完，自动死掉，那么就无法去处理信号了
#这个问题需要解决，如何让主进程的主线程不死掉！

#对于这个xumenger爬虫，因为要在result这个dict中处理数据，所以需要配置为单进程多线程的爬虫！
#不能配置为多进程的爬虫

if __name__ == '__main__':
    #爬虫run()之后，主线程也会进入循环，直到等待Ctrl-Z消息
    craw.run()
    
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

    ttagname = []
    tcount = []
    for tag in tagsort:
        tmp = unicode(tag[0], 'utf-8')
        ttagname.append(tmp)
        tcount.append(tag[1])

    tagname = tuple(ttagname)
    count = tuple(tcount)
    
    n_groups = 10
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    rects1 = plt.bar(index, count, alpha=opacity, color='r', label='Tag')

    plt.xlabel('Count')
    plt.ylabel('Tag')
    plt.title('xumenger\'s tag message')
    plt.xticks(index+bar_width, tagname)
    plt.ylim(0, 200)
    plt.legend()

    plt.tight_layout()
    plt.show()
