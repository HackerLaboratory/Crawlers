# -*- coding: utf-8 -*-

"""url管理器
* 用于管理未处理、已经处理的URL
* URL管理类是非线程安全的
"""
class UrlManager(object):

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        if url is None:
            return
        if (url not in self.new_urls) and (url not in self.old_urls):
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if (urls is None) or (0 == len(urls)):
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return (0 != len(self.new_urls))

    def get_new_url(self):
        if (0 < len(self.new_urls)):
            new_url = self.new_urls.pop()
            self.old_urls.add(new_url)
            return new_url
        else:
            return None
