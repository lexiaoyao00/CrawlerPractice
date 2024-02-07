import requests
from bs4 import BeautifulSoup
import re
import os

class MyImg():
    def __init__(self, filename, path=os.getcwd()):
        self._filename = filename
        self._path = path

class MySpider():
    def __init__(self,referer=None):
        self._session = requests.Session()
        if referer is not None:
            self._session.get(referer)

    @property
    def session(self):
        return self._session

    def get(self,url):
        self._response = requests.get(url)
        return self._response

    def post(self,url,data=None, json=None):
        return self._session.post(url,data,json)

    def save(self,filename:str,fileContent=None):
        if fileContent is None:
            fileContent=self._response
        with open(filename,'wb+') as f:
            f.write(fileContent.content)

