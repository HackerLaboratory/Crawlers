# -*- coding: utf-8 -*-

"""thread or process
True: multi threading
False: multi processing
"""
isMultiProcess = False

"""downloader count
downloader is thread or process
"""
downloaderCount = 1

"""timeout when download url
"""
downloadTimeout = 20

"""parser count
parser is thread or process
"""
parserCount = 1

"""outputer count
outputer is thread or process
"""
outputerCount = 1

"""URL regular expression
config URL regular expression and it's deal class name
"""
urlREs = {'http://www.xumenger.com/.*/': 'xumenger', 
          'http://www.xumenger.com/page.*': 'page'}

"""start URL
config one or more StartURL
"""
startUrls = ['http://www.xumenger.com', ]

"""except URL regular expression
when a crawler craw url/html, it will parse many urls
this config item used to all URLs that are not have to dealed
"""
exceptUrlREs = ['http://www.xumenger.com/tags.*',
              'http://www.xumenger.com/categories.*',
              'http://www.xumenger.com/download/.*',
              'http://www.xumenger.com/media/.*']
