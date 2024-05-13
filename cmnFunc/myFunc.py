import os
import SpiderCls.mySpider as myspi
from bs4 import BeautifulSoup
from cfg import config
import requests

mcfg_ini = config.Config("ini").get_Parser()
mcfg_yaml = config.Config("yaml").get_Parser()

def getproxyCgf(section = "proxy"):
    proxy_cfg ={}
    conf = mcfg_ini
    keys = conf.get_keys(section)
    for key in keys:
        proxy_cfg[key] = conf.get(section,key)

    return proxy_cfg

def getProxy(addr=None):
    proxies = None
    if addr is None:
        addr = getproxyCgf()["proxyget"]

    try:
        res = requests.get(addr)
    except Exception as e:
        print("未获取到代理:")
        print(e)
        print("********************************")
    else:
        proxy = res.json().get('proxy')
        proxies = {"http":"http://{}".format(proxy)}

    return proxies

def getDBCfg(section="database"):
    dbcfg= {
        'host': '',
        'port': '',
        'user': '',
        'pw': '',
        'db':'',
        'charset': ''
    }

    conf = mcfg_ini
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
    if(os.path.dirname(filePath) == ''): return
    if os.path.exists(os.path.dirname(filePath)):
        return
    else:
        os.makedirs(os.path.dirname(filePath))

def creatSpiderAndParseBs4(url,headers=None):
    spider = myspi.MySpider()
    res =  spider.get(url,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    return spider,soup



def testProscess():
    cfg = mcfg_ini.getInitCfg()
    print(cfg)