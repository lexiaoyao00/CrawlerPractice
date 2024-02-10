import cfg.ConfigurationOperation as mcf
from SpiderCls.mySpider import SpiderBase
import requests
import time
import js2py

#jb9网站js Base64.decode 返回decode函数
def Base64DeCode(filename):
    with open(filename,'r',encoding='utf-8') as jsf:
        js = jsf.read()
        b64 = js2py.eval_js(js)
        decode = b64.decode
        return decode

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
        self._videos =[]
        #视频网址解码函数
        self._funcDecode = Base64DeCode(r"js/jb9.js")
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
        linkCount = 0
        for a in links:
            # print(a["href"])
            # print(a["title"])
            if a["href"] in self._postsLinks or a["title"] in self._postTitles:
                print(f'{a["title"]}已存在')
                continue
            linkCount +=1
            self._postsLinks.append(a["href"])
            self._postTitles.append(a["title"])

        return linkCount

    # 获取大分类页面的下一页
    def getNextPageOfPosts(self,url,proxies=None):
        rule = "li.next-page a"
        self._rules["nextPOP"] = rule
        spi_postsPage = SpiderBase(self._rules["nextPOP"])
        linkList = spi_postsPage.urlParse(url=url,proxies=proxies)
        existsFlag = True
        if linkList:
            # print("link:",link)
            self._postsPages.append(linkList[0]['href'])
        else:
            print("该网页中未找到下一页标签",url)
            existsFlag = False

        return existsFlag

    # 获取资源页的图片链接
    def getImgsOfResource(self,url,proxies=None):
        rule = "div.gallery-item.gallery-fancy-item a"
        self._rules["imgs"] = rule
        spi_imgs = SpiderBase(self._rules['imgs'])
        img_links = spi_imgs.urlParse(url=url,proxies=proxies)

        # print(img_links)
        for link in img_links:
            print(link["href"])

        return len(img_links)

    # 获取资源页的视频链接
    def getVideoOfResource(self,url,proxies=None):
        rule = "div.article-video div"
        self._rules["videos"] = rule
        spi_postsPage = SpiderBase(self._rules["videos"])
        videos = spi_postsPage.urlParse(url=url,proxies=proxies)
        existsFlag = True
        if videos:
            # print("videos:",videos)
            # print("key:",videos[0]['data-key'])
            key = videos[0]['data-key']
            videoUrl = self._funcDecode(key)
            print("videoUrl:",videoUrl)
            self._videos.append(videoUrl)
        else:
            print("该网页中未找到视频",url)
            # self._videos.append("")
            existsFlag = False

        return existsFlag

def mainProcess():
    # key = "aHR0cHM6Ly90azkuZXMvd3AtY29udGVudC91cGxvYWRzLzIwMjQvMDEvMDA5NC5tcDQ="

    cfg = mcf.CfgOperation()
    addr = cfg.get("DEAFULT","proxyGet")
    # print("addr:",addr)

    j = JB9()
    j.getCfg(section="jb9")

    proxies = getProxy(addr)
    print("proxies:",proxies)
    j.getPosts(j._config["url"],proxies=proxies)
    # print(j._postsPages[0])
    # flg = True
    # while flg:
    #     index = len(j._postsPages) - 1
    #     flg = j.getNextPageOfPosts(j._postsPages[index])
    #     time.sleep(0.5)
    # j.getImgsOfResource(url = j._postsLinks[1],proxies=proxies)
    j.getVideoOfResource(url = j._postsLinks[1],proxies=proxies)


    # print(j._postsLinks)
    # print(j._postTitles)
    # print(j._postsPages)

