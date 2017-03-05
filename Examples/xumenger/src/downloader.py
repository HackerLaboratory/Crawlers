# -*- coding: utf-8 -*-

import urllib2

"""下载器

"""
class Downloader(object):
    
    def __init__(self):
        self.count = 1

    def download(self, url):
        if url is None:
            return None
        try:
            headers = {'User-Agent':  'Chrome/23.0.1271.64',
                      'Accept': 'text/html;q=0.9,*/*;q=0.8',
                      'Connection': 'close',
                      'Referer': None}
            timeout = 40
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, timeout=timeout)
            if (200 == response.getcode()):
                print self.count, ' | ', url
                self.count = self.count + 1
                html = response.read()
                return html
        except Exception as e:
            print '[', url, ']download error: ', e.message
            return None

