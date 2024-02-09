import cfg.ConfigurationOperation as myConf
import SpiderCls.mySpider as myspi
import os
import time
import requests
from bs4 import BeautifulSoup
import re
from cmnFunc import myFunc as mf
from concurrent.futures import ThreadPoolExecutor


g_myHeaders = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}

# 配置信息
g_cfg = {
    'resourceDir':'output',
    'referer':'',
    'url':'',
    'output':'',
    'maxPagenumber':0
}

def getCfg():
    """获取配置文件内容"""
    global g_cfg
    conf = myConf.CfgOperation()
    resourceDir = conf.get('DEAFULT','resourceDir')
    referer = conf.get('umei','referer')
    url = conf.get('umei','url')
    output = conf.get('umei','outputDir')
    maxPagenumber = conf.get('umei','maxPageOfSub')

    g_cfg['resourceDir'] = resourceDir
    g_cfg['referer']=referer
    g_cfg['url'] = url
    g_cfg['output'] = output
    g_cfg['maxPagenumber'] = int(maxPagenumber)


def mainPage():
    """获取大分类页面中的小分类页面网址
    大分类为： meinvtupian
    小分类为： xingganmeinv"""
    referer = g_cfg['referer']
    url = g_cfg['url']
    spi,soup = mf.creatSpiderAndParseBs4(url)

    subPageUrl = soup.find_all('h2')
    subUrlList = []
    for u in subPageUrl:
        # print(u)
        subUrl=referer + u.a.attrs['href']
        subUrlList.append(subUrl)

    return subUrlList

def getResourcePageUrl(soup: BeautifulSoup):
    """获取小分类页面中帖子的网址,每页算上重复的有30个"""
    referer = g_cfg['referer']
    itemsList = soup.find_all('div',attrs={'class':'img'})
    for item in itemsList:
        resourcePageUrl = referer + item.a.attrs['href']
        # print(resourcePageUrl)
        yield resourcePageUrl

def getResourcePageUrlOfNextPage(spider:myspi.MySpider, soup:BeautifulSoup):
    """获取小分类的下一个页面，如/meinvtupian/xingganmeinv 第二页"""
    referer = g_cfg['referer']
    nextPage = soup.find('div',attrs={'id':'pageNum'}).find_all('a')[-2]
    if nextPage.has_attr('class'):
        return None

    url_nextPage = referer + nextPage.attrs['href']
    nextPageSoup = spider.moveSpider(url_nextPage)
    nextPageItemsList = getResourcePageUrl(nextPageSoup)

    return nextPageSoup,nextPageItemsList


def subPage(url):
    """获取小分类页面中资源页面网址"""
    # 获取当前页中的所有资源页面网址
    index = 1
    spi,soup = mf.creatSpiderAndParseBs4(url)
    itemsGenerator = getResourcePageUrl(soup)
    resourcePageUrlList = []
    for item in itemsGenerator:
        resourcePageUrl = item
        # print(resourcePageUrl)
        resourcePageUrlList.append(resourcePageUrl)

    # print(resourcePageUrlList)
    # 获取下一页中的所有资源页面网址
    condition = True
    nextPageSoup = soup
    while condition==True:
        print('第{0}小分类页面已处理'.format(index))
        index +=1
        # print(resourcePageUrlList)
        yield resourcePageUrlList
        resourcePageUrlList.clear()
        nextPageSoup,nextPageItemsList = getResourcePageUrlOfNextPage(spi,nextPageSoup)
        for item in nextPageItemsList:
            resourcePageUrl = item
            resourcePageUrlList.append(resourcePageUrl)

        if nextPageItemsList is None:
            condition=False
        else:
            # time.sleep(1)
            continue

def getResource(spider:myspi.MySpider,soup:BeautifulSoup,justfilename):
    """保存图片资源"""
    imgSrc = soup.find('div',attrs={'class':r"big-pic"}).find('img').attrs['src']
    imgContent = spider.get(imgSrc)
    # print("imgSrc:",imgSrc)
    title = soup.find('h1').string
    fileExtension = imgSrc.split('.')[-1]
    fileFloder = os.path.join(g_cfg['resourceDir'],g_cfg['output'],title)
    # 创建目录，没有则不会创建
    mf.creatDir(fileFloder)
    filePath = os.path.join(fileFloder,justfilename+'.'+fileExtension)
    # filePath = 'output/img/' + title+'/'+justfilename+'.'+fileExtension
    # print("filePath:",filePath)
    spider.save(filePath,imgContent)
    return fileFloder

def getNextResourcePageUrl(soup:BeautifulSoup):
    """下一页的网址"""
    referer = g_cfg['referer']
    nextPage = soup.find('div',attrs={'class':'pages'}).find_all('li')[-2]
    finaPage = soup.find('div',attrs={'class':'pages'}).find_all('li')[-1]
    # print("nextPath:",nextPage)
    # print("finaPage:",finaPage)
    if nextPage.has_attr('class') or finaPage.has_attr('class'):
        nextPathUrl = None
    else:
        nextPathUrl = referer + nextPage.find('a').attrs['href']
    # print("nextPathUrl:",nextPathUrl)

    return nextPathUrl


def resourcePage(url:str):
    """处理资源页面,获取大图,返回图片数量"""
    spi,sp = mf.creatSpiderAndParseBs4(url,headers=g_myHeaders)

    # 下载图片
    firstFileName = url.split('/')[-1].split('.')[0]
    fileFloder = getResource(spi,sp,firstFileName)

    condition = True
    count = 1
    nextsoup = sp
    while condition==True:
        # 下一张图的位置
        nextUrl = getNextResourcePageUrl(nextsoup)
        if nextUrl is None:
            condition = False
            print(f"{fileFloder}下载完毕")
            continue
        nextsoup = spi.moveSpider(nextUrl)
        nextFileName = nextUrl.split('/')[-1].split('.')[0]
        fileFloder = getResource(spi,nextsoup,nextFileName)
        count += 1
        time.sleep(1)

    return count




def mainProcess():
    """主程序"""
    getCfg()
    subList = mainPage()
    url_xingganmeinv = subList[0]
    resourceUrlGen = subPage(url_xingganmeinv)

    # resourceUrlList = next(resourceUrlGen)
    # resourcePage(resourceUrlList[2])

    maxCount = g_cfg['maxPagenumber']
    index = 0
    flag = True
    while flag:
        if maxCount > 0 and maxCount <= index:
            print(f"{maxCount}页已下载完毕")
            flag = False
            continue

        resourceUrlList = next(resourceUrlGen)
        if resourceUrlList:
            with ThreadPoolExecutor(30) as t:
                for url in resourceUrlList:
                    t.submit(resourcePage,url)
        else:
            flag = False
            continue

        index += 1

