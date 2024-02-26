import tkinter as tk
from Spiders import danbooru


class Input(tk.Frame):
    def __init__(self,master,name:str,content=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.name= name
        self.content= content if content else ""
        self.create_widgets()

    def create_widgets(self):
        '''
        Label:标签控件,可以显示文本
        Entry：输入控件，用于显示简单的文本内容
        '''

        self.label = tk.Label(self,
                        wraplength=100,
                        justify="left",
                        anchor="w")
        self.label["text"] = self.name + ":"
        
        self.label.pack(side="left")

        # 绑定变量
        self.var = tk.Variable()

        self.entry = tk.Entry(self,textvariable=self.var) # show="*" 可以表示输入密码
        self.entry.pack(side="right",expand=True,fill="x")
        self.set_content(self.content)

    def set_content(self, content:str):
        self.var.set(content)

    def get_content(self):
        return self.entry.get()
    


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")

        self.create_widgets()

    def getTags(self,event=None):
        url = self.input.get_content()
        # url = "https://danbooru.donmai.us/posts/7261490"
        print(url)
        p = danbooru.PostPage(url)
        tags = p.obtainImageTags()
        self.set_value_of_text(','.join(tags))


    def create_widgets(self):
        self.create_input("帖子网址")
        self.create_text()
        self.create_button()


    def create_input(self,name:str):
        self.input = Input(self,name=name)
        self.input.pack(side="top",expand=True, fill="x",pady="5px")

    def create_button(self):
        self.bt_quit = tk.Button(self)
        self.bt_quit["text"] = "获取标签"
        self.bt_quit["command"] = self.getTags
        # self.bt_quit.bind("<Button-1>",self.getTags)
        self.bt_quit.pack(side="bottom",pady="5px")

    def create_text(self):
        '''
        文本控件：用于显示多行文本
        '''
        # height表示的是显示的行数
        self.text = tk.Text(self)

        self.text.pack(fill="both",pady="5px")

    def insert_to_text(self,value):
        self.text.insert(tk.INSERT, value)

    def set_value_of_text(self, value):
        self.text.delete("1.0","end")
        self.insert_to_text(value)



def mainProcess():
    # 创建主窗口
    root = tk.Tk()
    # 设置标题
    root.title("danbooru")
    # 设置大小和位置
    root.geometry("400x400+200+50")
    app = Application(master=root)
    app.mainloop()