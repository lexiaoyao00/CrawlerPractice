import os
import SpiderCls.mySpider as myspi
from bs4 import BeautifulSoup


def creatDir(path):
    if os.path.exists(path):
        return
    elif not os.path.isdir(path):
        os.makedirs(path)
    else:
        pass

def creatSpiderAndParseBs4(url):
    spider = myspi.MySpider()
    res =  spider.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    return spider,soup

def movePider(url,spider:myspi.MySpider):
    res =  spider.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    return soup