from SpiderCls.mySpider import SpiderBase
import cfg.ConfigurationOperation as mcf
from cmnFunc import myFunc as mf

class PostInfo:
    def __init__(self):
        self.artist = []
        self.copyright = []
        self.characters = []
        self.general = []
        self.meta = []
        self.img_information = {
            "ID": "",
            "Uploader": "",
            "Date": "",
            "Size": "",
            "Source": "",
            "Rating": "",
            "Score": "",
            "Favorites": "",
            "Status": ""
        }


class PostPage(PostInfo):
    rule_attrs = [
        "artist",
        "copyright",
        "characters",
        "general",
        "meta",
        "img_information"
    ]


    def __init__(self):
        super(PostPage, self).__init__()
        self._setGainRules()

    def _setGainRules(self):
        self.GainRules = {}
        self.GainRules[self.rule_attrs[3]] = "ul.general-tag-list li"

    def obtainImageInformation(self,postUrl:str):
        rule = self.GainRules[self.rule_attrs[3]]
        # print(rule)
        post_spider = SpiderBase(rule)
        res = post_spider.getPage(postUrl)
        # lis = post_spider.urlParse(postUrl,clash_proxies)
        # print(lis)

class Danbooru:
    def __init__(self):
        self.post_urls = []



def mainProcess():

    test_url = "https://danbooru.donmai.us/posts/7261490"
    # test_url = "https://www.whatismyip.com.tw/"
    # test_url="https://steamdb.info/"
    p1 = PostPage()
    p1.obtainImageInformation(test_url)
