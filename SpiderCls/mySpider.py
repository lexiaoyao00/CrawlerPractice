import requests
from bs4 import BeautifulSoup
import re
import os

class MyPage():
    def __init__(self,url:str,**kwargs):
        self._url = url

class MySpider():
    def __init__(self,referer=None):
        self._session = requests.Session()
        if referer is not None:
            self._session.get(referer)

    @property
    def session(self):
        return self._session

    def get(self,url,**kwargs):
        self._response = requests.get(url,**kwargs)
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

