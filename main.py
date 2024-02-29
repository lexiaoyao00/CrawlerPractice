import os
from cfg import config
from cmnFunc import myFunc

if __name__ == '__main__':
    process = "danbooru"
    match process:
        case "patreon":
            from Spiders import patreon
            patreon.mainProcess()
        case "danbooru":
            from gui import ui_danbooru
            from Spiders import danbooru
            ui_danbooru.mainProcess()
        case 'umei':
            from Spiders import umei
            umei.mainProcess()
        case 'jb9':
            from Spiders import jb9
            jb9.saveFromDbProscess()
        case 'test':
            myFunc.testProscess()
        case _:
            print("未指定程序")
            os.system('pause')