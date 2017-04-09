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

"""develop information:
    1. developer need to develop Parse、Output function
    2. Parse
        Args:
            html page string
        Returns:
            any kinds of content
    3. Output
        Args:
            content
        Returns:
            pass
"""

class xumenger(object):
    """xumenger class
    to craw www.xumenger.com to get tag information
    """

    def __init__(self):
        """xumenger constructor
        """
        self.pattern = re.compile(r'<a href="/tags/#(.*?)" title=.*?>')

    def Parse(self, html):
        """parse www.xumenger.com to get content
        """
        content = []
        tags = self.pattern.findall(html, re.S|re.M)
        if tags is not None:
            for tag in tags:
                content.append(tag)
        return content

    def Output(self, content):
        """output content
        """
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

class page(object):
    """page class use to deal www.xumenger.com/page.*
    
    it does not have to parse and output content
    just for get more urls
    """

    def Parse(self, html):
        return None

    def Output(self, content):
        pass

"""craw www.xumenger.com
use matplotlib to draw tag's distribution
because of using dict to manage output content, so xumenger have to config as multithreading
"""
if __name__ == '__main__':
    # craw start
    craw.run()
    # craw stop, deal result
    lock.acquire()
    try:
        # sort according dict
        tagDict = sorted(result.iteritems(), key=lambda d:d[1], reverse=True)
        tagList = []
        # in case sort's cout less than 10
        dictSize = 0;
        if len(tagDict) > 10:
            dictSize = 10
        else:
            dictSize = len(tagDict)
        for i in range(dictSize):
            tagList.append(tagDict[i])     
    finally:
        lock.release()
    # output tag's name and tag's count
    for tag in tagList:
        print tag[0], ':', tag[1]

    tagName = []
    tagCount = []
    for tag in tagList:
        tmp = unicode(tag[0], 'utf-8')
        tagName.append(tmp)
        tagCount.append(tag[1])
    name = tuple(tagName)
    count = tuple(tagCount)
    # use matplotlib to draw tag distribution
    groupCount = 10
    fig, ax = plt.subplots()
    index = np.arange(groupCount)
    barWidth = 0.35
    opacity = 0.4
    rects = plt.bar(index, count, alpha = opacity, color = 'r', label = 'Tag')
    # draw x, y label
    plt.xlabel('Tag')
    plt.ylabel('Count')
    plt.title('xumenger\'s tag message')
    plt.xticks(index + barWidth, name)
    plt.ylim(0, 200)
    plt.legend()
    # show
    plt.tight_layout()
    plt.show()

