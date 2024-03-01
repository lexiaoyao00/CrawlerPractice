import tkinter as tk
from Spiders import danbooru
from gui.comm_ui import Input,TextArea
import sys
import os



class PostPageApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.create_widgets()

        self.get_stdout_handle()


        self.post_obj=None

    def create_widgets(self):
        self.create_input()
        self.create_information_area()
        self.create_button()
        self.create_log_area()

        # testurl="https://danbooru.donmai.us/posts/7266628?q=order%3Arank"
        # self.input.set_content(testurl)


    def create_input(self):
        self.input_area = tk.Frame(self)
        self.input_url = Input(self.input_area,name="帖子网址")

        self.input_area.pack(side="top",expand=True, fill="x",pady="5px")

    def create_button(self):
        self.button_area = tk.Frame(self)
        self.bt_getinfo = tk.Button(self.button_area)
        self.bt_getinfo["text"] = "获取信息"
        self.bt_getinfo["command"] = self.getInfo
        self.bt_getinfo.pack(side="left",padx=10)

        self.bt_download = tk.Button(self.button_area)
        self.bt_download["text"] = "下载"
        self.bt_download["command"] = self.downloadPost
        self.bt_download.pack(side="left",padx=10)

        self.bt_filterImageGenerals = tk.Button(self.button_area)
        self.bt_filterImageGenerals["text"] = "过滤标签"
        self.bt_filterImageGenerals["command"] = self.filterPostGenerals
        self.bt_filterImageGenerals.pack(side="left",padx=10)



        self.button_area.pack(side="bottom",pady="5px")


    def create_information_area(self):
        self.info_area = tk.Frame(self)
        self.artist = TextArea(self.info_area,"Artist",height=1)
        self.copyright = TextArea(self.info_area,"Copyright",height=1)
        self.tags = TextArea(self.info_area,"Tags")
        self.information = TextArea(self.info_area,"Information",height=10)

        self.info_area.pack(fill="both",pady="5px")

    def create_log_area(self):
        self.log_area = TextArea(self,"Log",height=10)


    def clear_info(self):
        self.artist.clear_content()
        self.copyright.clear_content()
        self.tags.clear_content()
        self.information.clear_content()

    def clear_log(self):
        self.log_area.clear_content()

    def getInfo(self,event=None):
        url = self.input_url.get_content()
        if url is None or url == "":
            print("网址为空，请输入网址!")
        else:
            self.post_obj = danbooru.PostPage(url)
            artists = self.post_obj.obtainImageArtists()
            copyrights = self.post_obj.obtainImageCopyrights()
            characters = self.post_obj.obtainImageCharacters()
            generals = self.post_obj.obtainImageGenerals()
            Metas = self.post_obj.obtainImageMetas()
            informations=[]
            dict_info = self.post_obj.obtainImageInformation()

            for value in dict_info.values():
                informations.append(value)
            tags =characters+generals+Metas

            self.clear_info()
            if artists:
                self.artist.set_content(",".join(artists))
            if copyrights:
                self.copyright.set_content(",".join(copyrights))
            if tags:
                self.tags.set_content(",".join(tags))
            if informations:
                self.information.set_content("\n".join(informations))


    def downloadPost(self,event=None):
        if self.post_obj:
            try:
                url = self.post_obj.img_information["Url"]
                fileFloder = "output/danbooru/"
                fileName = self.post_obj.img_information["Name"]
                filePath = fileFloder + fileName
                self.post_obj.post_spider.download_from_url(filePath=filePath,url=url)

                print("成功下载")
                print("文件保存路径:",(os.getcwd() +os.path.sep+ filePath.replace("/",os.path.sep)))
            except Exception as e:
                print("Erro:",e)
                print("下载失败")
        else:
            print("请先获取信息")

    def filterPostGenerals(self,event=None):
        if self.post_obj:
            try:
                filte_tags = self.post_obj.filterImageTags()

                if self.tags:
                    self.tags.set_content(",".join(filte_tags))
            except Exception as e:
                print("Erro:",e)
                print("过滤失败")
        else:
            print("请先获取信息")

    def get_stdout_handle(self):
        sys.stdout = self.log_area


    def __del__(self):
        sys.stdout = self.log_area._console

class PopulorPageApp(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack(expand=True, fill="both")

        self.create_widgets()

    def create_widgets(self):
        self.create_input()

    def create_input(self):
        self.input_area = tk.Frame(self)
        self.input_date = Input(self.input_area,name="时间")


        self.input_area.pack(side="top",expand=True, fill="x",pady="5px")




def mainProcess():
    # 创建主窗口
    root = tk.Tk()
    # 设置标题
    root.title("danbooru")
    # 设置大小和位置
    # root.geometry("400x400+200+50")
    app = PostPageApp(master=root)
    # app = PopulorPageApp(master=root)
    app.mainloop()