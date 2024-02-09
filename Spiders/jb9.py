import cfg.ConfigurationOperation as mcf
from SpiderCls.mySpider import SpiderBase
import requests



def getProxy(addr):
    return requests.get(addr).json()

def popProxy(addr):
    return requests.get(addr).json()
class JB9:
    _config = {
        "resourceDir" : "output",
        "outputDir":"",
        "referer":"",
        "url":""
    }
    def __init__(self) -> None:
        # self._fistPageUrl = None
        self._rules = {}
        self._postsLink = []
        self._postTitle = []
    # def creatSpider(self):
    #     spider = SpiderBase()

    # 获取大分类页面的帖子链接和标题
    def getPosts(self,url,proxy=None):
        rule = "div.post.grid.grid-zz div.img a"
        self._rules['post'] = rule
        spi_imgPost = SpiderBase(self._rules['post'])
        links = spi_imgPost.urlParse(url=url,proxies=proxy)
        for a in links:
            # print(a["href"])
            # print(a["title"])
            if a["href"] in self._postsLink or a["title"] in self._postTitle:
                print(f'{a["title"]}已存在')
                continue

            self._postsLink.append(a["href"])
            self._postTitle.append(a["title"])


    def getCfg(self,section="DEAFULT"):
        conf = mcf.CfgOperation()
        self._config["outputDir"] = conf.get(section,"outputDir")
        self._config["referer"] = conf.get(section,"referer")
        self._config["url"] = conf.get(section,"url")





def mainProcess():
    cfg = mcf.CfgOperation()
    addr = cfg.get("DEAFULT","proxyGet")
    print("addr:",addr)

    j = JB9()
    j.getCfg(section="jb9")

    proxyJson = getProxy(addr)
    print(proxyJson)
    proxy = proxyJson.get("proxy")
    # print("proxy:",proxy)
    j.getPosts(j._config["url"],proxy={"http":"http://{}".format(proxy)})

    print(j._postsLink)

