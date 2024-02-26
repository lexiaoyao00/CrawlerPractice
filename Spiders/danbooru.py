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


    def __init__(self,postUrl:str):
        super(PostPage, self).__init__()
        self.url = postUrl
        self.post_spider = SpiderBase()
        self._setGainRules()

    def _setGainRules(self):
        self.GainRules = {}
        self.GainRules[self.rule_attrs[3]] = "ul.general-tag-list li"
        self.GainRules[self.rule_attrs[5]] = "section#post-information li"

    def obtainImageTags(self,postUrl:str=None):
        tags=[]
        url = postUrl if postUrl else self.url
        rule = self.GainRules[self.rule_attrs[3]]
        node_list = self.post_spider.urlParse(url=url,gainRuleCss=rule)

        tags = [a.select_one("a.search-tag").text for a in node_list]
        # print(tags)

        return tags


    def obtainImageInformation(self,postUrl:str=None):

        url = postUrl if postUrl else self.url
        rule = self.GainRules[self.rule_attrs[5]]
        node_list = self.post_spider.urlParse(url=url,gainRuleCss=rule)

class Danbooru:
    def __init__(self):
        self.post_urls = []



def mainProcess():

    test_url = "https://danbooru.donmai.us/posts/7261490"
    p1 = PostPage(test_url)
    p1.obtainImageTags()
