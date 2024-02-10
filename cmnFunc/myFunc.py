import os
import SpiderCls.mySpider as myspi
from bs4 import BeautifulSoup
import cfg.ConfigurationOperation as mcf


def getDBCfg(section="database"):
    dbcfg= {
        'host': '',
        'port': '',
        'user': '',
        'pw': '',
        'db':'',
        'charset': ''
    }

    conf = mcf.CfgOperation()
    dbcfg['host'] = conf.get(section,'host')
    dbcfg['port'] = int(conf.get(section,'port'))
    dbcfg['user'] = conf.get(section,'user')
    dbcfg['pw'] = conf.get(section,'pw')
    dbcfg['db'] = conf.get(section,'db')
    dbcfg['charset'] = conf.get(section,'charset')

    return dbcfg

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