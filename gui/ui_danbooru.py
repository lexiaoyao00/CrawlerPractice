import tkinter as tk
from Spiders import danbooru
from gui.comm_ui import Input,TextArea
import sys
import os
import io
import time
from PIL import Image, ImageTk
from urllib.request import urlopen

current_file_dir = os.path.dirname(__file__)

class PostPageApp(tk.Frame):
    title = "帖子页分析"
    _lastPage = None
    def __init__(self, master,defalt_url:str|None=None):
        super().__init__(master)
        self.now_url = defalt_url
        self.create_widgets()
        self.get_stdout_handle()

        self.post_obj=None

        global last_ui
        self._lastPage = last_ui
        last_ui=PostPageApp

        self.pack(expand=True, fill="both")

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(expand=True, fill="both")

    def back(self):
        self.hide()
        self._lastPage(self.master).show()


    def create_widgets(self):
        self.create_input()
        self.create_button()
        self.create_information_area()
        self.create_log_area()

        # testurl="https://danbooru.donmai.us/posts/7266628?q=order%3Arank"
        # self.input_url.set_content(testurl)


    def create_input(self):
        self.input_area = tk.Frame(self)
        self.input_url = Input(self.input_area,name="帖子网址")
        
        if self.now_url:
            self.input_url.set_content(self.now_url)
            self.now_url = None

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

        self.bt_back = tk.Button(self.button_area)
        self.bt_back["text"] = "上一页面"
        self.bt_back["command"] = self.back
        self.bt_back.pack(side="left",padx=10)


        self.button_area.pack(side="bottom",pady="5px")


    def create_information_area(self):
        self.info_area = tk.Frame(self)
        self.artist = TextArea(self.info_area,"Artist",height=1)
        self.copyright = TextArea(self.info_area,"Copyright",height=1)
        self.tags = TextArea(self.info_area,"Tags")
        self.information = TextArea(self.info_area,"Information",height=10)

        self.info_area.pack(expand=True,fill="both",pady="5px")

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
    title = "欢迎页分析"
    _geometry = "800x800"
    _lastPage = None
    tk_image_list = []
    posts_list = []
    def __init__(self,master):
        super().__init__(master)
        master.geometry(self._geometry)
        self.matrix_area = tk.Frame(self)
        self.create_widgets()
        self.pack(expand=True, fill="both")

        global last_ui
        self._lastPage = last_ui
        last_ui=PopulorPageApp

    def hide(self):
        self.pack_forget()

    def show(self):
        self.draw_matrix(self.matrix_area,self.tk_image_list,self.posts_list)
        self.pack(expand=True, fill="both")

    def back(self):
        self.hide()
        self._lastPage(self.master).show()


    def create_widgets(self):
        self.create_input()
        self.create_button()
        # self.create_matrix()

    def create_input(self):
        self.input_area = tk.Frame(self)

        self.input_date = Input(self.input_area,name="时间")
        now_time = time.strftime("%Y-%m-%d", time.localtime()) 
        self.input_date.set_content(now_time)

        self.input_pagenumber = Input(self.input_area,name="页数")
        self.input_pagenumber.set_content("1")

        self.input_scale = Input(self.input_area,name="规模")
        self.input_scale.set_content("day")

        self.input_area.place(x=10,y=10)

    
    def draw_matrix(self,master,preview_image_list,post_url_list):
        canvas = tk.Canvas(master,height=600)
        scro = tk.Scrollbar(master)
        scro.pack(side='right',fill='y')
        canvas.pack(fill="both")
        # Frame作为容器放置组件
        self.posts_area = tk.Frame(canvas)
        self.posts_area.pack(fill="both",expand=True)
        # 将posts_area添加至Canvas上
        canvas.create_window((0,0),window=self.posts_area)
        
        # 绑定鼠标滚轮
        self.master.bind("<MouseWheel>",lambda event:canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        count = 0
        for post_img_pre in preview_image_list:
            m_col = count%5
            m_row = int(count/5)
            m_post_url = post_url_list[count]
            img_label = tk.Label(self.posts_area,
                               image=post_img_pre,
                            #    text=count,
                            #    bg="red",
                               width=130,
                               height=180)
            
            img_label.bind("<Button-1>",lambda event:self.newPost(url=m_post_url))

            img_label.grid(row=m_row,column=m_col)

            count +=1

         # 更新posts_area大小，不然没有滚动效果
        self.posts_area.update()
        # 将滚动按钮绑定只Canvas上
        canvas.configure(yscrollcommand=scro.set, scrollregion=canvas.bbox("all"))
        # canvas.bind("<MouseWheel>", processWheel)
        scro.config(command=canvas.yview)

    def create_matrix(self):
        self.matrix_area.destroy()
        self.tk_image_list.clear()
        self.posts_list.clear()


        self.matrix_area = tk.Frame(self,height=600)

        m_date = self.input_date.get_content()
        m_pagenumber = self.input_pagenumber.get_content()
        m_scale = self.input_scale.get_content()

        m_posts = self.getPosts(m_date,m_pagenumber,m_scale)

        for post in m_posts:
            m_post_url = post["href"]
            m_preview_url = post["preview_imgUrl"]
            # print(m_preview_url)
            img_bytes = self.populor_obj.populorPage_spider.get(m_preview_url).content
            pil_img = Image.open(io.BytesIO(img_bytes))
            self.tk_image_list.append(ImageTk.PhotoImage(pil_img))
            self.posts_list.append(m_post_url)


        self.draw_matrix(self.matrix_area,self.tk_image_list,self.posts_list)

        self.matrix_area.pack(side="top",expand=True, fill="x",pady="5px")

    def create_button(self):
        self.button_area = tk.Frame(self)

        self.bt_obtain = tk.Button(self.button_area)
        self.bt_obtain["text"] = "获取"
        self.bt_obtain["command"] = self.create_matrix
        self.bt_obtain.pack(side="left",padx=10)


        self.bt_back = tk.Button(self.button_area)
        self.bt_back["text"] = "上一页面"
        self.bt_back["command"] = self.back
        self.bt_back.pack(side="right",padx=10)


        self.button_area.pack(side="top",pady="5px")

    def getPosts(self,date:str=None,pageNum:int|str=None,scale:str=None):
        self.populor_obj = danbooru.PopulorPage(date=date,pageNum=pageNum,scale=scale)
        self.all_posts = self.populor_obj.obtainPostInfo()

        return self.all_posts
    
    def newPost(self,url:str):
        self.hide()
        PostPageApp(self.master,url).show()



class ShowPage():
    _area :tk.Frame = None
    _root :tk.Tk = None
    def __init__(self,master:tk.Tk,newGeometry=None):
        self._root = master
        self._root.title('主页面')
        # self.root.geometry('800x800')
        self._root.geometry(newGeometry)
        self.now_window :tk.Frame =None
        


        if not self.now_window:
            self.create_widgets()

    def hide(self):
        self._area.pack_forget()

    def show(self):
        global last_ui
        last_ui = ShowPage
        self._area.pack(side="top", fill="both", expand=True,pady="5px")

    def create_widgets(self):
        self.create_area()
        
    def show_window(self,page_ui:tk.Frame,newTitle:str):
        if self.now_window:
            self.hide_window()
        
        self._root.title(newTitle)
        self.now_window=page_ui(self._root)
        self.now_window.show()

    def hide_window(self):
        if self.now_window:
            self.now_window.hide()
        else:
            pass

    def create_area(self):
        self._area = tk.Frame(self._root)

        self.bt_post = tk.Button(self._area)
        self.bt_post["text"] = "post"
        self.bt_post["command"] = self.show_window_post
        self.bt_post.pack(side="bottom",padx=10)

        self.bt_populor = tk.Button(self._area)
        self.bt_populor["text"] = "populor"
        self.bt_populor["command"] = self.show_window_populor
        self.bt_populor.pack(side="bottom",padx=10)


        self._area.pack(side="top", fill="both", expand=True,pady="5px")

    def show_window_post(self):
        self._area.destroy()
        self.show_window(PostPageApp,PostPageApp.title)

    def show_window_populor(self):
        self._area.destroy()
        self.show_window(PopulorPageApp,PopulorPageApp.title)




last_ui=ShowPage

def mainProcess():
    # 创建主窗口
    main_window = tk.Tk()
    main_window.geometry("800x800")
    wm = ShowPage(main_window)
    # wm.show_window(PostPageApp,PostPageApp.title)
    # wm.hide_window()
    # wm.show_window(PopulorPageApp,PopulorPageApp.title)
    main_window.mainloop()