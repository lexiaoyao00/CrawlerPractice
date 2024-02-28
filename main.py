import os
from cfg import config
from gui import ui_danbooru
from Spiders import umei,jb9,danbooru
from cmnFunc import myFunc

if __name__ == '__main__':
    process = "danbooru"
    match process:
        case "danbooru":
            ui_danbooru.mainProcess()
        case 'umei':
            umei.mainProcess()
        case 'jb9':
            jb9.saveFromDbProscess()
        case 'test':
            myFunc.testProscess()
        case _:
            print("未指定程序")
            os.system('pause')