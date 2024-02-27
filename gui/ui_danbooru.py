import tkinter as tk
from Spiders import danbooru
from gui.comm_ui import Input,TextArea
import sys



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.create_widgets()

        self.get_stdout_handle()

    def create_widgets(self):
        self.create_input("帖子网址")
        self.create_information_area()
        self.create_button()
        self.create_log_area()

        # testurl="https://danbooru.donmai.us/posts/7266628?q=order%3Arank"
        # self.input.set_content(testurl)


    def create_input(self,name:str):
        self.input = Input(self,name=name)
        self.input.pack(side="top",expand=True, fill="x",pady="5px")

    def create_button(self):
        self.bt_quit = tk.Button(self)
        self.bt_quit["text"] = "获取标签"
        self.bt_quit["command"] = self.getTags
        # self.bt_quit.bind("<Button-1>",self.getTags)
        self.bt_quit.pack(side="bottom",pady="5px")

    def create_information_area(self):
        self.info_area = tk.Frame(self)
        self.artist = TextArea(self.info_area,"Artist",height=1)
        self.copyright = TextArea(self.info_area,"Copyright",height=1)
        self.tags = TextArea(self.info_area,"Tags")
        self.information = TextArea(self.info_area,"Information",height=10)

        self.info_area.pack(fill="both",pady="5px")

    def create_log_area(self):
        self.log_area = TextArea(self,"Log")

    
    def clear_info(self):
        self.artist.clear_content()
        self.copyright.clear_content()
        self.tags.clear_content()
        self.information.clear_content()

    def getTags(self,event=None):
        url = self.input.get_content()
        if url is None or url == "":
            print("网址为空，请输入网址!")
        else:
            # url = "https://danbooru.donmai.us/posts/7261490"
            p = danbooru.PostPage(url)
            artists = p.obtainImageArtists()
            copyrights = p.obtainImageCopyrights()
            characters = p.obtainImageCharacters()
            generals = p.obtainImageGenerals()
            Metas = p.obtainImageMetas()
            informations=[]
            dict_info = p.obtainImageInformation()
            
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



    def get_stdout_handle(self):
        sys.stdout = self.log_area


    def __del__(self):
        sys.stdout = self.log_area._console





def mainProcess():
    # 创建主窗口
    root = tk.Tk()
    # 设置标题
    root.title("danbooru")
    # 设置大小和位置
    # root.geometry("400x400+200+50")
    app = Application(master=root)
    app.mainloop()