import cfg.ConfigurationOperation as mc
from SpiderCls.mySpider import SpiderBase


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
    def getPosts(self,url):
        rule = "div.post.grid.grid-zz div.img a"
        self._rules['post'] = rule
        spi_imgPost = SpiderBase(self._rules['post'])
        links = spi_imgPost.urlParse(url=url)
        for a in links:
            # print(a["href"])
            # print(a["title"])
            if a["href"] in self._postsLink or a["title"] in self._postTitle:
                print(f'{a["title"]}已存在')
                continue

            self._postsLink.append(a["href"])
            self._postTitle.append(a["title"])


    def getCfg(self,section="DEAFULT"):
        conf = mc.CfgOperation()
        self._config["outputDir"] = conf.get(section,"outputDir")
        self._config["referer"] = conf.get(section,"referer")
        self._config["url"] = conf.get(section,"url")





def mainProcess():
    j = JB9()
    j.getCfg(section="jb9")
    j.getPosts(j._config["url"])

    print(j._postsLink)

