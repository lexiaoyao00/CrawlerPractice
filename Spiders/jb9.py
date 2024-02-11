import cfg.ConfigurationOperation as mcf
from SpiderCls.mySpider import SpiderBase
from db.DBCls import Database as db
from cmnFunc import myFunc as mf
import requests
import time
import js2py
import os
import threading
from concurrent.futures import ThreadPoolExecutor

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

    rule_attrs = [
        "posts",
        "nextPageOfPosts",
        "imgs",
        "video",
        "videoMenu"
    ]

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

        self._setGainRules()
    # def creatSpider(self):
    #     spider = SpiderBase()
    def getCfg(self,section="DEAFULT"):
        conf = mcf.CfgOperation()
        self._config["outputDir"] = conf.get(section,"outputDir")
        self._config["referer"] = conf.get(section,"referer")
        self._config["url"] = conf.get(section,"url")
        self._postsPages.append(self._config["url"])


    def _setGainRules(self):
        rule_posts= "div.post.grid.grid-zz div.img a"
        rule_nextPost = "li.next-page a"
        rule_imgs = "div.gallery-item.gallery-fancy-item a"
        rule_video = "div.article-video div"
        rule_videoMenu = "div.article-video div.videos-menu a"

        self._rules[self.rule_attrs[0]] = rule_posts
        self._rules[self.rule_attrs[1]] = rule_nextPost
        self._rules[self.rule_attrs[2]] = rule_imgs
        self._rules[self.rule_attrs[3]] = rule_video
        self._rules[self.rule_attrs[4]] = rule_videoMenu

    # 获取大分类页面的帖子链接和标题
    def getPosts(self,url,proxies=None):
        spi_imgPost = SpiderBase(self._rules[self.rule_attrs[0]])
        links = spi_imgPost.urlParse(url=url,proxies=proxies)
        postsCount = 0
        if not links:
            print("当前页面没找到帖子")
            return postsCount
        
        for a in links:
            # print(a["href"])
            # print(a["title"])
            if a["href"] in self._postsLinks or a["title"] in self._postTitles:
                print(f'{a["title"]}已存在')
                continue
            postsCount +=1
            self._postsLinks.append(a["href"])
            self._postTitles.append(a["title"])

        print(url,"页面帖子数量:",postsCount)
        return postsCount

    # 获取大分类页面的下一页
    def getNextPageOfPosts(self,url,proxies=None):
        spi_postsPage = SpiderBase(self._rules[self.rule_attrs[1]])
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
        spi_imgs = SpiderBase(self._rules[self.rule_attrs[2]])
        img_links = spi_imgs.urlParse(url=url,proxies=proxies)

        # print(img_links)
        if img_links:
            for link in img_links:
                # print(link["href"])
                self._imgs.append(link["href"])
        else:
            print("当前帖子中未找到图片")

        print("当前帖子找到图片 ",len(img_links)," 张")
        return len(self._imgs)

    # 获取资源页的视频链接
    def getVideoOfResource(self,url,proxies=None):
        spi_videoMenu = SpiderBase(self._rules[self.rule_attrs[4]])
        videoMenu = spi_videoMenu.urlParse(url=url,proxies=proxies)

        if videoMenu:
            for a in videoMenu:
                url_videoIndex = a["href"]
                spi_videos = SpiderBase(self._rules[self.rule_attrs[3]])
                videos = spi_videos.urlParse(url=url_videoIndex,proxies=proxies)
                key = videos[0]["data-key"]
                videoUrl = self._funcDecode(key)
                self._videos.append(videoUrl)
            
            print("当前帖子中找到视频")

        else:
            spi_video = SpiderBase(self._rules[self.rule_attrs[3]])
            videos = spi_video.urlParse(url=url,proxies=proxies)
            if videos:
                key = videos[0]['data-key']
                videoUrl = self._funcDecode(key)
                print("当前帖子中找到视频")
                self._videos.append(videoUrl)
            else:
                print("当前帖子中未找到视频")
                # self._videos.append("")

        return len(self._videos)

    # 保存帖子链接到数据库
    def savePostsLink(self,conn:db):
        val_obj_post = {
            "title": "",
            "link":"",
            "is_download": "0"
        }

        lengthPosts = len(self._postsLinks)
        # print("lengthPosts:",lengthPosts)
        for i in range(lengthPosts):
            val_obj_post["link"] = repr(self._postsLinks[i])
            val_obj_post["title"] = repr(self._postTitles[i])

            # print("val_obj_post:",val_obj_post)

            insert_id = conn.insert("jb9_posts",val_obj_post)

        return insert_id
    
    # 保存图片链接到数据库
    def saveImgsLink(self,conn:db,post_title:str):
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
    
    # 保存视频链接到数据库
    def saveVideosLink(self,conn:db,post_title:str):
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

        if not self._videos:
            # print("请先获取视频链接")
            return False
        for i in range(lengthvideos):
            val_obj_videos["name"] = repr(self._videos[i].split('/')[-1])
            val_obj_videos["link"] = repr(self._videos[i])
            val_obj_videos['posts_id'] = str(post_id)


            insert_id = conn.insert("jb9_videos",val_obj_videos)

        return insert_id

    #保存一个图片到本地
    def saveOneImgTlLocal(self,url:str,title,proxies=None):
        spi_img = SpiderBase()
        spi_img.get(url=url,proxies=proxies)
        filepath = os.path.join("output","jb9",title)
        mf.creatDir(filepath)
        filename = os.path.join(filepath,url.split("/")[-1])
        spi_img.save(filename)

    # 保存当前存入的图片
    def saveImgsToLocal(self,title,proxies=None):
        if not self._imgs:
            print("当前对象未获取图片链接")
        else:
            with ThreadPoolExecutor(30) as t:
                for u in self._imgs:
                    t.submit(self.saveOneImgTlLocal,u,title,proxies)

            print("当前存入的图片已保存完毕")

    # 保存当前存入的视频
    def saveVideosToLocal(self,title,proxies=None):
        spi_video = SpiderBase()
        if not self._videos:
            print("当前对象未获取视频链接")
        else:
            for u in self._videos:
                filepath = os.path.join("output","jb9",title)
                mf.creatDir(filepath)
                filename = os.path.join(filepath,u.split("/")[-1])
                spi_video.save_bigFlow(fielname=filename,url=u,proxies=proxies)

            print("当前存入的视频已保存完毕")






def mainProcess():
    my_dbcfg = mf.getDBCfg()
    print("database config:",my_dbcfg)
    my_db = db(my_dbcfg)

    my_cfg = mcf.CfgOperation()
    addr = my_cfg.get("DEAFULT","proxyGet")
    # print("addr:",addr)

    j = JB9()
    j.getCfg(section="jb9")

    flg = True
    while flg:
        page_index = len(j._postsPages) - 1

        proxies = getProxy(addr)
        print("proxies:",proxies)

        flg = j.getNextPageOfPosts(j._postsPages[page_index])
        time.sleep(0.5)
        j.getPosts(j._postsPages[page_index],proxies=proxies)
        j.savePostsLink(my_db)

        post_index = 0
        post_num = len(j._postsLinks)
        # TODO 测试完记得删掉这行
        post_num = 3
        while post_index < post_num:
            title = j._postTitles[post_index]
            link = j._postsLinks[post_index]
            print("当前帖子标题:",title)
            print("当前帖子链接:",link)

            j.getImgsOfResource(url =link ,proxies=proxies)
            j.getVideoOfResource(url =link,proxies=proxies)

            # print("正在保存视频链接到数据库")
            # j.saveVideosLink(my_db,title)
            # print("正在保存图片链接到数据库")
            # j.saveImgsLink(my_db,title)


            thread_svtl = threading.Thread(target=j.saveVideosToLocal,kwargs ={"title":title,"proxies":proxies})
            print("正在保存视频")
            thread_svtl.start()
            print("正在保存图片")
            j.saveImgsToLocal(title=title,proxies=proxies)

            # 等待线程结束
            thread_svtl.join()

            post_index+=1

            # 清除当前帖子的媒体信息
            j._imgs.clear()
            j._videos.clear()


        # 清除当前页面中的帖子信息
        j._postsLinks.clear()
        j._postTitles.clear()

        # TODO 测试完记得删掉这行
        flg = False


    print("page number:",len(j._postsPages))

