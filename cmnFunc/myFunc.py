import os
import SpiderCls.mySpider as myspi
from bs4 import BeautifulSoup


def creatDir(floderPath:str):
    if os.path.exists(floderPath):
        return
    # elif not os.path.isfile(path):
    #     os.makedirs(os.path.dirname(path))
    else:
        os.makedirs(floderPath)

def creatDirOfFile(filePath:str):
    if os.path.exists(filePath):
        return
    else:
        os.makedirs(os.path.dirname(filePath))

def creatSpiderAndParseBs4(url,headers=None):
    spider = myspi.MySpider()
    res =  spider.get(url,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    return spider,soup