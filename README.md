##项目简介

Python爬虫框架和使用该框架实现的各种爬虫。对应Python版本是Python2

##背景介绍

互联网上存在海量的数据，Python在互联网时代有很多天然的优势：

* 有诸多Python开发的Web框架：django、flask、web.py等，可以方便的拿来做Web开发
* Python开发爬虫也有天然的优势，比如自带的urllib、urllib2、htmlparser、re等模块，还有很多的第三方开发包，比如Requests、Beautiful Soup、lxml等，可以很方便的处理HTTP、下载网页、解析网页等
* Python在数据分析方面也有很强的优势，比如可以使用Numpy、matplotlib、pandas等包对爬下来的数据进行数据分析、处理，通过图表等方式进行人性化的展示
* 当然对于用爬虫爬取并分析的数据，还可以用Python进行Web开发来在网站上展示数据的分析结果

可以看到Python在爬虫、数据分析、开发Web网站展示数据等全流程上发挥作用

以上是我个人对于Python的一些思考，也正是基于如此的原因才激发我学习Python的兴趣

然而光学习而不动手的话，当时学到的东西很快就遗忘了，尤其是在计算机领域，单纯的学习Python语法、了解Python并没有什么用处，必须实实在在的用Python做出来东西才是最好的深刻学习Python的方法，不光是Python，计算机领域的诸多应用层面都应该如此：编程、调试、设计……

一直对Python爬虫比较感兴趣，在[《Python网络爬虫简单架构》](http://www.xumenger.com/python-spider-20160608/)、[《Python网络爬虫概述》](http://www.xumenger.com/python-crawler-20170102/)两篇文章中对于Python爬虫的简单逻辑、涉及到的各个方面进行了比较全面的讲述，所以计划基于这两篇文章的思想实现一个简单的爬虫框架

开发的过程中必然会遇到各种问题，必须去逐个针对性的解决，这也正是为什么实践是最好的学习方法的原因所在：遇到问题，思考应该用什么知识解决这个问题，再去针对性地学习这方面知识

针对开发过程中遇到的Python方面的问题、对应的解决方法，会在我的个人博客[http://www.xumenger.com/](http://www.xumenger.com/)中对应进行系统化地整理

##爬虫架构

