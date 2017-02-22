# -*- coding: utf-8 -*-

import urllib
import urllib2

"""下载器

"""
class Downloader(object):
    
    def __init__(self):
        pass

    def download(self, url):
        if url is None:
            return None
        try:
            response = urllib2.urlopen(url)
            if (200 == response.getcode()):
                html = response.read()
                return html
        except Exception as e:
            print '[', url, ']download error: ', e.message
            return None
