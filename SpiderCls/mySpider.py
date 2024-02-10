import requests
from bs4 import BeautifulSoup
import re
import os
import random
from cfg import ConfigurationOperation as mcf
import time


user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                    ]

# 基本属性
class SpiderBase():
    def __init__(self,gainRuleCss=None):
        self._headers = {
            # "User-Agent": random.choice(user_agent_list),
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            'Connection': 'close',
            "Cookie":"zh_choose=s; zh_choose=s; _pk_id.5.6a12=94f02e8f6a5092ad.1707481555.; sitetips=1"
        }
        # 新建会话
        self._session = requests.Session()
        # 解析规则 css选择器 如 div.big_pic
        self._gainRule = gainRuleCss
        # 标签列表 存放需要的标签 如<img src="example.jpg">
        self._gainElem = {}
        # 网址列表 存放同一系列网址
        self._urlList = []

        self._response = None

    # get方法
    def get(self,url:str,proxies=None,**kwargs):
        kwargs.setdefault("allow_redirects", True)

        proxies = proxies or {}
        retry_count = 5
        while retry_count>0:
            try:
                self._response = self._session.get(url,headers=self._headers,proxies=proxies,**kwargs)
                return self._response
            except Exception:
                retry_count -=1
                time.sleep(3)
                print("尝试重新连接")

        return requests.Response()

    # post方法
    def post(self,url,data=None, json=None,**kwargs):
        return self._session.post(url,data,json,**kwargs)


    # 解析
    def urlParse(self,url,proxies=None):
        resContent = self.get(url,proxies)
        if resContent.status_code != 200:
            print("something went wrong,status code of response:",resContent.status_code)
            print("The problematic url:",url)
        resContent.encoding = 'utf-8'
        soup = BeautifulSoup(resContent.text,"lxml")
        if not self._gainRule:
            print("当前爬虫无解析数据")
            nodeList = []
        else:
            nodeList  = soup.select(self._gainRule)
        # for node in nodeList:
        #     print(node)
        return nodeList

    def xmlParse(self,xml):
        pass

    # 资源保存
    def save(self,filename:str,fileContent=None):
        if fileContent is None and self._response is None:
            print("请先请求网址")
            return
        elif fileContent is None:
            fileContent=self._response
        else:
            pass

        with open(filename,'wb+') as f:
            f.write(fileContent.content)

    #用来保存视频之类的大文件
    def save_bigFlow(self,fielname:str,url:str,proxies=None,**kwargs):
        r = self.get(url=url,proxies=proxies,stream = True,**kwargs)
        f = open(fielname,'wb+')
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)

        f.close()


class SpiderSecend(SpiderBase):
    def initSpider(self,url):
        pass



class MySpider():
    def __init__(self,referer=None):
        self._session = requests.Session()
        if referer is not None:
            self._session.get(referer)

    @property
    def session(self):
        return self._session

    def get(self,url,**kwargs):
        self._response = self._session.get(url,**kwargs)
        return self._response

    def post(self,url,data=None, json=None,**kwargs):
        return self._session.post(url,data,json,**kwargs)

    def save(self,filename:str,fileContent=None):
        if fileContent is None:
            fileContent=self._response
        with open(filename,'wb+') as f:
            f.write(fileContent.content)

    def moveSpider(self,url:str):
        res =  self.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,'lxml')

        return soup

