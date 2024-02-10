import cfg.ConfigurationOperation as mcf
from SpiderCls.mySpider import SpiderBase
from db.DBCls import Database as db
from cmnFunc import myFunc as mf
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
        self._imgs = []
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
        postsCount = 0
        for a in links:
            # print(a["href"])
            # print(a["title"])
            if a["href"] in self._postsLinks or a["title"] in self._postTitles:
                print(f'{a["title"]}已存在')
                continue
            postsCount +=1
            self._postsLinks.append(a["href"])
            self._postTitles.append(a["title"])

        return postsCount

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
        if img_links:
            for link in img_links:
                # print(link["href"])
                self._imgs.append(link["href"])
        else:
            print("该网页中未找到视频",url)

        return len(img_links)

    # 获取资源页的视频链接
    def getVideoOfResource(self,url,proxies=None):
        rule = "div.article-video div"
        self._rules["videos"] = rule
        spi_postsPage = SpiderBase(self._rules["videos"])
        videos = spi_postsPage.urlParse(url=url,proxies=proxies)
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

        return len(videos)

    def savePostsLink(self,conn:db):
        # 保存帖子链接到数据库
        val_obj_post = {
            "title": "",
            "link":"",
            "is_download": "0"
        }

        lengthPosts = len(self._postsLinks)
        print("lengthPosts:",lengthPosts)
        for i in range(lengthPosts):
            val_obj_post["link"] = repr(self._postsLinks[i])
            val_obj_post["title"] = repr(self._postTitles[i])

            print("val_obj_post:",val_obj_post)

            insert_id = conn.insert("jb9_posts",val_obj_post)

        return insert_id
    
    def saveImgsLink(self,conn:db,post_title:str):
        # 保存图片链接到数据库
        val_obj_imgs = {
            "name": "",
            "link":"",
            "is_download": "0",
            "posts_id":"0"
        }

        # 查询帖子id
        table = "jb9_posts"
        factor_str = "title = " + repr(post_title)
        post_id = conn.select_one(table,factor_str,"id").get('id')
        lengthImgs = len(self._imgs)

        if not self._imgs:
            print("请先获取图片链接")
            return False
        for i in range(lengthImgs):
            # print("image link :",self._imgs[i])
            val_obj_imgs["name"] = repr(self._imgs[i].split('/')[-1])
            val_obj_imgs["link"] = repr(self._imgs[i])
            val_obj_imgs['posts_id'] = str(post_id)
            # print("val_obj_imgs:",val_obj_imgs)

            insert_id = conn.insert("jb9_imgs",val_obj_imgs)

        return insert_id

    def saveVideosLink(self,conn:db,post_title:str):
        # 保存视频链接到数据库
        val_obj_videos = {
            "name": "",
            "link":"",
            "is_download": "0",
            "posts_id":"0"
        }

        # 查询帖子id
        table = "jb9_posts"
        factor_str = "title = " + repr(post_title)
        post_id = conn.select_one(table,factor_str,"id").get('id')

        lengthvideos = len(self._videos)
        for i in range(lengthvideos):
            val_obj_videos["name"] = repr(self._videos[i].split('/')[-1])
            val_obj_videos["link"] = repr(self._videos[i])
            val_obj_videos['posts_id'] = str(post_id)


            insert_id = conn.insert("jb9_videos",val_obj_videos)

        return insert_id

    # 保存链接到数据库
    def saveLink2DB(self,conn:db):
        pass




def mainProcess():
    my_dbcfg = mf.getDBCfg()
    print("database config:",my_dbcfg)
    my_db = db(my_dbcfg)

    my_cfg = mcf.CfgOperation()
    addr = my_cfg.get("DEAFULT","proxyGet")
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
    # j.getVideoOfResource(url = j._postsLinks[1],proxies=proxies)

    # insert_id = j.savePostsLink(my_db)
    # print("insert_id:",insert_id)
    index = 1
    imgs_len = j.getImgsOfResource(url = j._postsLinks[index],proxies=proxies)
    videos_len = j.getVideoOfResource(url = j._postsLinks[index],proxies=proxies)
    # print("imgs_len:",imgs_len)
    print("videos_len:",videos_len)
    # insert_id = j.saveImgsLink(my_db,j._postTitles[index])
    insert_id = j.saveVideosLink(my_db,j._postTitles[index])


    # print(j._postsLinks)
    # print(j._postTitles)
    # print(j._postsPages)

