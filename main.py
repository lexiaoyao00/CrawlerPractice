import tkinter as tk

from gui import ui_danbooru
from Spiders import umei,jb9,danbooru
from cmnFunc import myFunc as mf

if __name__ == '__main__':
    test = 'danbooru'
    match test:
        case "danbooru":
            # danbooru.mainProcess()
            ui_danbooru.mainProcess()
        case 'test':
            mf.testProscess()
        case 'umei':
            umei.mainProcess()
        case 'jb9':
            jb9.saveFromDbProscess()
        case _:
            print("未指定程序")