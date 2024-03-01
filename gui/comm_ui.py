import tkinter
import sys
from typing import Literal
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
    
    def __init__(self,master,name:str,content=None,height=5,state:Literal["normal","disabled"]="disabled"):
        super().__init__(master)
        self.pack(expand=True, fill="both",pady="5px")
        self.height=height
        self.name= name
        self.content= content if content else ""
        self.state = state
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

        self.text = tkinter.Text(self,height=self.height,state=self.state)

        self.text.pack(expand=True,fill="both")
    
    def write(self,content:str):
        # nowtime = datetime.datetime.now()
        line =content
        if self.state == "normal":
            self.text.insert(tkinter.END, line)
        else:
            self.text["state"] = "normal"
            self.text.insert(tkinter.END, line)
            self.text.see(tkinter.END)
            self.text["state"] = self.state


    def flush(self):
        pass
        
    def reset(self):
        sys.stdout=self._console

    def set_content(self, content:str):
        if self.state == "normal":
            self.text.delete("1.0","end")
            self.text.insert(tkinter.INSERT,content)
        else:
            self.text["state"] = "normal"
            self.text.delete("1.0","end")
            self.text.insert(tkinter.INSERT, content)
            self.text["state"] = self.state


    def get_content(self,index1=0.0, index2=tkinter.END):
        self.content = self.text.get(index1,index2)
        return self.content
    
    def clear_content(self):
        if self.state == "normal":
            self.text.delete("1.0","end")
        else:
            self.text["state"] = "normal"
            self.text.delete("1.0","end")
            self.text["state"] = self.state
