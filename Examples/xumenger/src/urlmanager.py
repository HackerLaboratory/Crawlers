# -*- coding: utf-8 -*-

class UrlManager(object):
    """url manager
    use this class object to manage url
    new_urls is a list contain urls which are not dealed
    old_urls is a list contain urls which are dealed
    this class is not thread safe
    """

    def __init__(self):
        """urlmanager constructor
        """
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        """add a url to urlmanager
        in this method, judge url is dealed or not dealed

        Args:
            url: a url
        """
        if url is None:
            return
        if (url not in self.new_urls) and (url not in self.old_urls):
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """add a new url list to urlmanager
        
        Args:
            urls: a url list    
        """
        if (urls is None) or (0 == len(urls)):
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        """judge is there any url which is not dealed in urlmanager

        Returns:
            url count in new_urls
        """
        return (0 != len(self.new_urls))

    def get_new_url(self):
        """get url which is not dealed in urlmanager

        Returns:
            url: url which is not dealed
            None: if urlmanager do not have url which is not dealed
        """
        if (0 < len(self.new_urls)):
            new_url = self.new_urls.pop()
            self.old_urls.add(new_url)
            return new_url
        else:
            return None

