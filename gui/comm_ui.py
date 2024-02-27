import tkinter
import sys
import datetime

class Input(tkinter.Frame):

    def __init__(self,master,name:str,content=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.name= name
        self.content= content if content else ""
        self.pack_widgets()

    def pack_widgets(self):
        '''
        Label:标签控件,可以显示文本
        Entry：输入控件，用于显示简单的文本内容
        '''

        self.label = tkinter.Label(self,
                        wraplength=100,
                        justify="left",
                        anchor="w")
        self.label["text"] = self.name + ":"
        
        self.label.pack(side="left")

        # 绑定变量
        self.var = tkinter.Variable()

        self.entry = tkinter.Entry(self,textvariable=self.var) # show="*" 可以表示输入密码
        self.entry.pack(side="right",expand=True,fill="x")
        self.set_content(self.content)

    def set_content(self, content:str):
        self.var.set(content)

    def get_content(self):
        return self.entry.get()
    
class TextArea(tkinter.Frame):
    _console=sys.stdout
    
    def __init__(self,master,name:str,content=None,height=5):
        super().__init__(master)
        self.pack(expand=True, fill="both",pady="5px")
        self.height=height
        self.name= name
        self.content= content if content else ""
        self.pack_widgets()

    def pack_widgets(self):
        self.label = tkinter.Label(self,
                        width=10,
                        height=self.height,
                        wraplength=100,
                        justify="left",
                        anchor="w")
        self.label["text"] = self.name + ":"
        
        self.label.pack(side="left")

        self.text = tkinter.Text(self,height=self.height)

        self.text.pack(expand=True,fill="both")
    
    def write(self,content:str):
        # nowtime = datetime.datetime.now()
        line =content
        self.text.insert(tkinter.INSERT, line)

    def flush(self):
        pass
        
    def reset(self):
        sys.stdout=self._console

    def set_content(self, content:str):
        self.text.delete("1.0","end")
        self.text.insert(tkinter.INSERT,content)

    def get_content(self):
        self.content = self.text.get()
        return self.content
    
    def clear_content(self):
        self.text.delete("1.0","end")