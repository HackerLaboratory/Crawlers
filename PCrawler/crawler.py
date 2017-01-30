# -*- coding: utf-8 -*-

# html下载器
import urllib2

class HtmlDownloader(object):
	# 下载url指向的页面html内容
	def download(self, url):
		if url is None:
			return None
		
		# 使用urllib2模块下载url指向的html内容
		response = urllib2.urlopen(url)
		# 如果http的返回码不是200，说明请求下载失败
		if 200 != response.getcode():
			return None
		# 否则返回下载好的内容
		return response.read()

# html解析器
from bs4 import BeautifulSoup
import re
import urlparse

class HtmlParser(object):
	# 获取当前页面中的词条url列表
	def _get_new_url(self, page_url, soup):
		# 用一个集合存储本html中所有的词条url
		new_urls = set()

		# 需要匹配的url格式：/view/数字.htm
		links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))
		for link in links:
			new_url = link['href']		#此时获取的是不完全的url，比如/view/123.htm
			new_full_url = urlparse.urljoin(page_url, new_url)
			new_urls.add(new_full_url)
		return new_urls

	# 解析数据，需要解析标题和简介两个数据
	def _get_new_data(self, page_url, soup):
		# 用一个字典存储标题和简介数据
		res_data = {}
		
		# url也存放到字典中，方便使用
		res_data['url'] = page_url


