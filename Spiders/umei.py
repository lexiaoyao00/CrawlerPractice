import cfg.ConfigurationOperation as myConf
import SpiderCls.mySpider as myspi
import os
from bs4 import BeautifulSoup
import re
from cmnFunc import myFunc as mf
import time

cfg = {
    'referer':'',
    'url':''
}

def getCfg():
    global cfg
    conf = myConf.CfgOperation()
    referer = conf.get('umei','referer')
    url = conf.get('umei','url')
    cfg['referer']=referer
    cfg['url'] = url


def getResourcePageUrl(soup: BeautifulSoup):
    referer = cfg['referer']
    itemsList = soup.find_all('div',attrs={'class':'img'})
    for item in itemsList:
        resourcePageUrl = referer + item.a.attrs['href']
        # print(resourcePageUrl)
        yield resourcePageUrl

def mainPage():
    referer = cfg['referer']
    url = cfg['url']
    spi,soup = mf.creatSpiderAndParseBs4(url)

    subPageUrl = soup.find_all('h2')
    subUrlList = []
    for u in subPageUrl:
        # print(u)
        subUrl=referer + u.a.attrs['href']
        subUrlList.append(subUrl)

    return subUrlList



def getResourcePageUrlOfNextPage(spider:myspi.MySpider, soup:BeautifulSoup):
    referer = cfg['referer']
    nextPage = soup.find('div',attrs={'id':'pageNum'}).find_all('a')[-2]
    if nextPage.has_attr('class'):
        return None

    url_nextPage = referer + nextPage.attrs['href']
    nextPageSoup = mf.movePider(url_nextPage,spider)
    nextPageItemsList = getResourcePageUrl(nextPageSoup)

    return nextPageSoup,nextPageItemsList


def subPage(url):
    # 获取当前页中的所有资源页面网址
    index = 1
    spi,soup = mf.creatSpiderAndParseBs4(url)
    itemsGenerator = getResourcePageUrl(soup)
    resourcePageUrlList = []
    for item in itemsGenerator:
        resourcePageUrl = item
        # print(resourcePageUrl)
        resourcePageUrlList.append(resourcePageUrl)

    # 获取下一页中的所有资源页面网址
    condition = True
    nextPageSoup = soup
    while condition==True:
        index +=1
        # print(resourcePageUrlList)
        yield resourcePageUrlList
        print('第{0}页正在处理'.format(index))
        nextPageSoup,nextPageItemsList = getResourcePageUrlOfNextPage(spi,nextPageSoup)
        for item in nextPageItemsList:
            resourcePageUrl = item
            resourcePageUrlList.append(resourcePageUrl)

        if nextPageItemsList is None:
            condition=False
        else:
            # condition=False
            # time.sleep(1)
            continue




def resourcePage():
    pass

def mainPro():
    getCfg()
    subList = mainPage()
    # print(subList)
    url_xingganmeinv = subList[0]
    resourceUrlGen = subPage(url_xingganmeinv)
    # print(resourceUrlGen)
    # time.sleep(100)


    mf.creatDir('output')
    for i in range(20):
        resourceUrlList = next(resourceUrlGen)
        with open('./output/resourceUrlList.txt','w+',encoding='utf-8') as f:
            for url in '\n'.join(resourceUrlList):
                f.write(str(url))
