# -*- coding: utf-8 -*-

import re
import urlparse

class Parser(object):
    """parser class
    use this class object, parse html to get urls and content
    parse html use regular expression
    """

    def __init__(self, urlREs, exceptUrlREs):
        """parser constructor
        
        Args:
            urlREs: urls regular expression that this crawler have to deal 
            exceptUrlREs: urls regular expression this crawler do not have to deal
        """
        self.urlREs = urlREs
        self.exceptUrlREs = exceptUrlREs

    def isExceptURL(self, url):
        """judge this url is have to deal
        if this url match exceptUrlREs's item, return True

        Args: 
            url: a url
        Returns: 
            True: this url do not have to deal
            False: this url have to deal
        """
        for exceptUrl in self.exceptUrlREs:
            pattern = re.compile(exceptUrl)
            if pattern.match(url) is not None:
                return True
        return False

    def parseURL(self, urlHtml):
        """parse HTML
        this method parse html to get urls
        
        Args:
            urlHtml: a list include url and html
                item[0] is url
                item[1] is html
        Returns:
            a list include urls that is parsed from this html
        """
        new_urls = []
        url = urlHtml[0]
        html = urlHtml[1]

        # use regular pattern to parse html get all urls
        pattern = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        urls = pattern.findall(html)
        for u in urls:
            # get full url
            full_url = urlparse.urljoin(url, u)
            # judge this url is included in exceptUrlREs
            if not self.isExceptURL(full_url):
                # judge this url is included in urlREs
                for k in self.urlREs.keys():
                    pattern = re.compile(k)
                    if pattern.match(full_url) is not None:
                        new_urls.append(full_url)

        return new_urls

