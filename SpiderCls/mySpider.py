from curl_cffi import requests
# import requests
from bs4 import BeautifulSoup
import re
import os
import random
import time
from cmnFunc import myFunc as mf
import sys


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
    complete_URL=""
    def __init__(self,gainRuleCss=None,headers=None):
        """
        gainRuleCss:CSS选择器规则
        headers:请求头
        """
        if headers is None:
            self._headers = {
                "User-Agent": random.choice(user_agent_list),
                # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            }
        else:
            self._headers = headers
        # 新建会话
        self._session = requests.Session()
        # 解析规则 css选择器 如 div.big_pic
        self._gainRule = gainRuleCss
        # 标签列表 存放需要的标签 如<img src="example.jpg">
        self._gainElem = {}
        # 网址列表 存放同一系列网址
        self._urlList = []

        self._response = None

    def setGainRule(self, gainRuleCss):
        self._gainRule = gainRuleCss

    # get方法
    def get(self,url:str,proxies=None,**kwargs):
        kwargs.setdefault("allow_redirects", True)

        proxies = proxies or {}
        retry_count = 5
        while retry_count>0:
            try:
                self._response = self._session.get(url,headers=self._headers,proxies=proxies,impersonate="chrome116",**kwargs)
                self.complete_URL = self._response.url
                return self._response
            except Exception:
                retry_count -=1
                time.sleep(3)
                print("尝试重新连接")
        print("网页连接失败:",url)
        return requests.Response()
    
    # 拿到网页内容
    def getPage(self,url:str,proxies=None,savefile = False,filename="mypage.html",**kwargs):
        print("正在获取网页：",url)
        resContent = self.get(url=url,proxies=proxies,**kwargs)
        if resContent.text:
            print("网页内容已获取",self.complete_URL)
            if savefile:
                resContent.encoding = "utf-8"
                with open(filename,"w+",encoding="utf-8") as f:
                    f.write(resContent.text)
        else:
            print("未获取到网页内容")

        return resContent

    # post方法
    def post(self,url,data=None, json=None,**kwargs):
        return self._session.post(url,data,json,**kwargs)


    def pageParse(self,pageContent:requests.Response,encoding="utf-8",gainRuleCss=None):
        gainRule = gainRuleCss if gainRuleCss else self._gainRule
        pageContent.encoding = encoding
        soup = BeautifulSoup(pageContent.text,"lxml")
        if gainRule is None:
            print("当前无解析选择器规则")
            nodeList = []
        else:
            nodeList  = soup.select(gainRule)
        # for node in nodeList:
        #     print(node)
        return nodeList


    # 解析
    def urlParse(self,url,proxies=None,gainRuleCss = None,**kwargs):
        gainRule = gainRuleCss if gainRuleCss else self._gainRule
        resContent = self.get(url,proxies,**kwargs)
        if resContent.status_code != 200:
            print("something went wrong,status code of response:",resContent.status_code)
            print("The problematic url:",url)
        resContent.encoding = 'utf-8'
        soup = BeautifulSoup(resContent.text,"lxml")
        if gainRule is None:
            print("当前无解析选择器规则")
            nodeList = []
        else:
            nodeList  = soup.select(gainRule)
        # for node in nodeList:
        #     print(node)
        return nodeList

    def xmlParse(self,xml):
        pass

    # 资源保存
    def save(self,filename:str,responseContent=None):
        mf.creatDirOfFile(filename)
        if responseContent is None and self._response is None:
            print("请先请求网址，使用getPage方法")
            return
        elif responseContent is None:
            responseContent=self._response
        else:
            pass

        with open(filename,'wb+') as f:
            f.write(responseContent.content)

    #用来保存视频之类的大文件
    def save_bigFlow(self,filename:str,url:str,proxies=None,**kwargs):
        r = self.get(url=url,proxies=proxies,stream = True,**kwargs)
        f = open(filename,'wb+')
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)

        f.close()

    def download_from_url(self,filePath:str,url:str,proxies=None,**kwargs):
        mf.creatDirOfFile(filePath)

        res = self.get(url=url,proxies=proxies,**kwargs)
        with open(filePath,'wb+') as f:
            f.write(res.content)


class Downloader(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def start(self):
        res_length = requests.get(self.url, stream=True)
        total_size = int(res_length.headers['Content-Length'])
        print(res_length.headers)
        print(res_length)
        if os.path.exists(self.file_path):
            temp_size = os.path.getsize(self.file_path)
            print("当前：%d 字节， 总：%d 字节， 已下载：%2.2f%% " % (temp_size, total_size, 100 * temp_size / total_size))
        else:
            temp_size = 0
            print("总：%d 字节，开始下载..." % (total_size,))

        headers = {'Range': 'bytes=%d-' % temp_size,
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
        res_left = requests.get(self.url, stream=True, headers=headers)

        with open(self.file_path, "ab") as f:
            for chunk in res_left.iter_content(chunk_size=1024):
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()

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

