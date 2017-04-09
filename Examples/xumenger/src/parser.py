# -*- coding: utf-8 -*-

import re
import urlparse

"""解析器
解析HTML获取其中的
"""
class Parser(object):

    def __init__(self, reURLs, exceptURLs):
        self.reURLs = reURLs
        self.exceptURLs = exceptURLs

    def isExceptURL(self, url):
        for e in self.exceptURLs:
            pattern = re.compile(e)
            if pattern.match(url) is not None:
                return True
        return False

    def parseURL(self, urlHtml):
        new_urls = []
        url = urlHtml[0]
        html = urlHtml[1]
        #使用正则表达式获取网页中所有URL链接
        pattern = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        urls = pattern.findall(html)
        for u in urls:
            #拼接成完整的URL
            full_url = urlparse.urljoin(url, u)
            #判断该URL是否在exceptURLs中的配合，需过滤
            if not self.isExceptURL(full_url):
                #判断该URL是否符合在config.py中的reURLs配置
                for k in self.reURLs.keys():
                    pattern = re.compile(k)
                    if pattern.match(full_url) is not None:
                        new_urls.append(full_url)
        return new_urls

