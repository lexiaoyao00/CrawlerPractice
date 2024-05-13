from Spiders import *
import re
from enum import Enum,unique

@unique
class Clarity(Enum):
    """视频清晰度"""
    WORST = 0
    BEST = -1

class  VideoPage():

    m3u8_prefix = "https://surrit.com/"
    m3u8_playList_suffix = "/playlist.m3u8"
    m3u8_video_suffix = "/video.m3u8"
    m3u8_fileName = "missav.m3u8"
    reObj_m3u8_playListKey = re.compile(r'urls: .*?sixyik.com\\/(?P<playListKey>.*?)\\/seek.*?,',re.S)
    reObj_m3u8_videoSuffix = re.compile(r'^(?P<videoClarity>.*?)/video.m3u8',re.M)

    def __init__(self,url:None|str):
        self.url = url
        self.spider = SpiderBase()
        self.pageContent = self.spider.getPage(self.url)

        if self.pageContent == None: raise ValueError("网页内容未获取到")

        self.videoKW = ""
        self.videoUrl_M3U8 = None

    #m3u8网址的关键词 类似： 5164f6dd-3b1c-4480-aed8-48611c7349a0
    def _videoKW(self):
        self.textContent = self.pageContent.text
        self.videoKW = VideoPage.reObj_m3u8_playListKey.search(self.textContent).group("playListKey")
        return self.videoKW


    #获取playlist.m3u8
    def _playList(self):
        try:
            playListKey = self._videoKW()

        except Exception as e:
            playListKey = "error"
            raise e
        finally:
            result_playlist = VideoPage.m3u8_prefix + playListKey + VideoPage.m3u8_playList_suffix

            return result_playlist

    #通过playlist获取视频清晰度
    def _videoClarity(self):
        textContent_videoClarity = self.spider.getPage(self._playList()).text
        videoClarity = VideoPage.reObj_m3u8_videoSuffix.findall(textContent_videoClarity)
        return videoClarity

    #视频m3u8网址
    def VideoAddress(self,clarity:Clarity = Clarity.BEST):
        videoClarity = self._videoClarity()[clarity.value]
        self.videoUrl_M3U8:str = VideoPage.m3u8_prefix + "/"+ self.videoKW +"/" + videoClarity + VideoPage.m3u8_video_suffix
        
        #保存到本地
        self.spider.save(VideoPage.m3u8_fileName,self.spider.getPage(self.videoUrl_M3U8))

        return self.videoUrl_M3U8

    #保存m3u8视频
    def SaveVideoM3U8(self):
        with open(VideoPage.m3u8_fileName,mode='r',encoding='utf8') as f:
            for line in f:
                line = line.strip() # 去掉空格，空白，换行符
                if line.startswith("#"):
                    continue
                
                #视频片段网址
                if (self.videoUrl_M3U8):
                    prefix = self.videoUrl_M3U8.rsplit("/",1)[0]
                else:
                    # raise Exception("需要先获取视频网址")
                    self.VideoAddress()
                    prefix = self.videoUrl_M3U8.rsplit("/",1)[0]

                videoClipsUrl = prefix +"/"+ line

                #下载视频片段
                #TODO: 用多线程实现，现在是测试阶段
                # resp =  requests.get(videoClipsUrl)
                # with open("output/videoClips/" + line,mode="wb") as testFile:
                #     testFile.write(resp.content)
                # resp.close()




def mainProcess():
    testUrl = missav_url + '/dldss-298'

    vp = VideoPage(testUrl)
    vp.SaveVideoM3U8()


    print("missav Over")