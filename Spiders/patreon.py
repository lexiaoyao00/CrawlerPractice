from SpiderCls.mySpider import SpiderBase

class Collection():
    def __init__(self,url:str):
        self.url = url
        self.spider = SpiderBase()
        self._setGainRules()
        self.pageContent = self.spider.getPage(self.url)

    def _setGainRules(self):
        self.GainRules = {}


def mainProcess():
    url = "https://www.patreon.com/collection/128213"
    c = Collection(url)
    c.spider.getPage(url,None,True)