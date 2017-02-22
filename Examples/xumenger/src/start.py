# -*- coding: utf-8 -*-

import crawler

craw = crawler.Crawler(globals())


class xumenger(object):    
    def Parse(self, html):
        print 'xumenger.Parse'

    def Output(self, content):
        print 'xumenger.Output'

class page(object):
    def Parse(self, html):
        print 'page.Parse'

    def Output(self, content):
        print 'page.Output'


if __name__ == '__main__':
    craw.run()
