import cfg.ConfigurationOperation as mcf
from SpiderCls.mySpider import SpiderBase
import requests



def getProxy(addr):
    proxies = None
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
        self._postsPages =[]
        self._postsLinks = []
        self._postTitles = []
    # def creatSpider(self):
    #     spider = SpiderBase()
    def getCfg(self,section="DEAFULT"):
        conf = mcf.CfgOperation()
        self._config["outputDir"] = conf.get(section,"outputDir")
        self._config["referer"] = conf.get(section,"referer")
        self._config["url"] = conf.get(section,"url")
        self._postsPages.append(self._config["url"])

    # 获取大分类页面的帖子链接和标题
    def getPosts(self,url,proxies=None):
        rule = "div.post.grid.grid-zz div.img a"
        self._rules['post'] = rule
        spi_imgPost = SpiderBase(self._rules['post'])
        links = spi_imgPost.urlParse(url=url,proxies=proxies)
        for a in links:
            # print(a["href"])
            # print(a["title"])
            if a["href"] in self._postsLinks or a["title"] in self._postTitles:
                print(f'{a["title"]}已存在')
                continue

            self._postsLinks.append(a["href"])
            self._postTitles.append(a["title"])

    # 获取大分类页面的下一页
    def getNextPageOfPosts(self,url,proxies=None):
        rule = "li.next-page a"
        self._rules["nextPOP"] = rule
        spi_postsPage = SpiderBase(self._rules["nextPOP"])
        link = spi_postsPage.urlParse(url=url,proxies=proxies)
        if link:
            # print("link:",link)
            self._postsPages.append(link[0]['href'])



def mainProcess():
    cfg = mcf.CfgOperation()
    addr = cfg.get("DEAFULT","proxyGet")
    # print("addr:",addr)

    j = JB9()
    j.getCfg(section="jb9")

    proxies = getProxy(addr)
    print("proxies:",proxies)
    j.getPosts(j._config["url"],proxies=proxies)
    # print(j._postsPages[0])
    j.getNextPageOfPosts(j._postsPages[0])

    print(j._postsLinks)
    print(j._postTitles)
    print(j._postsPages)

