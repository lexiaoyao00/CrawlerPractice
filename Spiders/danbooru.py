from SpiderCls.mySpider import SpiderBase
import cfg.ConfigurationOperation as mcf
from cmnFunc import myFunc as mf

class PostInfo:
    def __init__(self):
        self.artists = []
        self.copyrights = []
        self.characters = []
        self.generals = []
        self.metas = []
        self.img_information = {
            "Url":"",
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
        self.pageContent = self.post_spider.getPage(self.url,savefile=True)

    def _setGainRules(self):
        self.GainRules = {}
        self.GainRules[self.rule_attrs[0]] = "ul.artist-tag-list li"
        self.GainRules[self.rule_attrs[1]] = "ul.copyright-tag-list li"
        self.GainRules[self.rule_attrs[2]] = "ul.character-tag-list li"
        self.GainRules[self.rule_attrs[3]] = "ul.general-tag-list li"
        self.GainRules[self.rule_attrs[4]] = "ul.meta-tag-list li"
        self.GainRules[self.rule_attrs[5]] = "section#post-information"

    def obtainImageArtists(self):
        rule = self.GainRules[self.rule_attrs[0]]
        node_list = self.post_spider.pageParse(pageContent=self.pageContent,gainRuleCss=rule)

        if node_list:
            self.artists = [a.select_one("a.search-tag").text for a in node_list]
        else:
            print("获取节点为空:",rule)

        return self.artists


    def obtainImageCopyrights(self,page:str=None):
        rule = self.GainRules[self.rule_attrs[1]]
        node_list = self.post_spider.pageParse(pageContent=self.pageContent,gainRuleCss=rule)

        if node_list:
            self.copyrights = [a.select_one("a.search-tag").text for a in node_list]
        else:
            print("获取节点为空:",rule)


        return self.copyrights

    def obtainImageCharacters(self,page:str=None):
        rule = self.GainRules[self.rule_attrs[2]]
        node_list = self.post_spider.pageParse(pageContent=self.pageContent,gainRuleCss=rule)

        if node_list:
            self.characters = [a.select_one("a.search-tag").text for a in node_list]
        else:
            print("获取节点为空:",rule)

        return self.characters

    def obtainImageGenerals(self,page:str=None):
        rule = self.GainRules[self.rule_attrs[3]]
        node_list = self.post_spider.pageParse(pageContent=self.pageContent,gainRuleCss=rule)

        if node_list:
            self.generals = [a.select_one("a.search-tag").text for a in node_list]
        else:
            print("获取节点为空:",rule)
        
        return self.generals
    
    def obtainImageMetas(self,page:str=None):
        rule = self.GainRules[self.rule_attrs[4]]
        node_list = self.post_spider.pageParse(pageContent=self.pageContent,gainRuleCss=rule)

        if node_list:
            self.metas = [a.select_one("a.search-tag").text for a in node_list]
        else:
            print("获取节点为空:",rule)


        return self.metas 


    def obtainImageInformation(self,page:str=None):
        rule = self.GainRules[self.rule_attrs[5]]
        node_list = self.post_spider.pageParse(pageContent=self.pageContent,gainRuleCss=rule)
        
        if node_list:
            img_ID = node_list[0].select_one("li#post-info-id").text.replace(" ","").replace("\n","")
            img_Uploader =  node_list[0].select_one("li#post-info-uploader").text.replace(" ","").replace("\n","")
            img_Date =  node_list[0].select_one("li#post-info-date").text.replace(" ","").replace("\n","")
            img_Size =  node_list[0].select_one("li#post-info-size").text.replace(" ","").replace("\n","")
            img_Url = node_list[0].select_one("li#post-info-size").select_one("a").get("href").replace(" ","").replace("\n","")
            img_Source =  node_list[0].select_one("li#post-info-source").text.replace(" ","").replace("\n","")
            img_Rating =  node_list[0].select_one("li#post-info-rating").text.replace(" ","").replace("\n","")
            img_Score =  node_list[0].select_one("li#post-info-score").text.replace(" ","").replace("\n","")
            img_Favorites =  node_list[0].select_one("li#post-info-favorites").text.replace(" ","").replace("\n","")
            img_Status =  node_list[0].select_one("li#post-info-status").text.replace(" ","").replace("\n","")
        else:
            img_ID = ""
            img_Uploader = ""
            img_Date = ""
            img_Size = ""
            img_Url = ""
            img_Source = ""
            img_Rating = ""
            img_Score = ""
            img_Favorites = ""
            img_Status = ""
            print("获取节点为空",rule)



        # infos = [str(a) for a in node_list]

        self.img_information["Url"] = img_Url
        self.img_information["ID"] = img_ID
        self.img_information["Uploader"] = img_Uploader
        self.img_information["Date"] = img_Date
        self.img_information["Size"] = img_Size
        self.img_information["Source"] = img_Source
        self.img_information["Rating"] = img_Rating
        self.img_information["Score"] = img_Score
        self.img_information["Favorites"] = img_Favorites
        self.img_information["Status"] = img_Status

        return self.img_information

class Danbooru:
    def __init__(self):
        self.post_urls = []



def mainProcess():

    test_url = "https://danbooru.donmai.us/posts/7261490"
    p1 = PostPage(test_url)
    p1.obtainImageGenerals()
