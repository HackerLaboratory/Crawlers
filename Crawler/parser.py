-*- coding: utf-8 -*-

import re
import urlparse

"""
解析器
"""

class Parser(object):

    def __init__(self, reURLs):
        self.reURLs = reURLs

    def parseURL(self, html):
        new_urls = []
        url = html[0]
        pageHtml = html[1]
        #使用正则表达式获取网页中所有URL链接
        pattern = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        urls = pattern.findall(pageHtml)
        for u in urls:
            #拼接成完整的URL
            new_full_url = urlparse.urljoin(url, u)
            #判断该URL是否符合在config.py中的reURLs配置
            for k in self.reURLs.keys():
                pattern = re.compile(k)
                if pattern.match(new_full_url) is not None:
                    print new_full_url
                    new_urls.append(new_full_url)
        return new_urls


