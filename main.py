import os
from cfg import config
from cmnFunc import myFunc

if __name__ == '__main__':
    cfgINI = config.Config('ini').get_Parser()
    process = None
    if cfgINI.has_section("initCfg"):
        process = cfgINI.get("initCfg","ExecuteProgram")
    else:
        raise ValueError("配置文件参数出错")
    
    process = "sstm" #TODO 测试用
    match process:
        case "sstm":
            from Spiders import sstm
            sstm.mainProcess()
        case "patreon":
            from Spiders import patreon
            patreon.mainProcess()
        case "danbooru":
            from gui import ui_danbooru
            from Spiders import danbooru
            # danbooru.mainProcess()
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