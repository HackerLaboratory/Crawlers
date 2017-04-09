# -*- coding: utf-8 -*-

import urllib2

class Downloader(object):
    """downloader class
    use this class object, download html according url
    download html use urllib2
    """
    
    def __init__(self):
        """downloader constructor
        """
        self.count = 1

    def download(self, url, timeout=10):
        """download html according to url
        
        Args:
            url: a url to download
            timeout: download html timeout
        Returns:
            url corresponding to html
            if download error or exception, return None
        Raises:
            download exception
        """
        if url is None:
            return None
        try:
            headers = {'User-Agent': 'Chrome/23.0.1271.64',
                      'Accept': 'text/html;q=0.9,*/*;q=0.8',
                      'Connection': 'close',
                      'Referer': None}
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, timeout=timeout)
            errcode = response.getcode()
            if (200 == errcode):
                print '[', self.count, '] ', url
                self.count = self.count + 1
                html = response.read()
                return html
            else:
                print 'download error, errcode=', errcode, 'url=', url
                return None
        except Exception as e:
            print 'download exception: ', e.message, 'url=', url
            return None

