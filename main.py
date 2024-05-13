import os
from cfg import config
from cmnFunc import myFunc
import argparse

argParser = argparse.ArgumentParser()


def getargs():
    argParser.add_argument("--process",default=None,required=False)

    return argParser.parse_args()

def main(process:str|None = None):
    if process is None:
        cfgINI = config.Config('ini').get_Parser()
        if cfgINI.has_section("initCfg"):
            process = cfgINI.get("initCfg","ExecuteProgram")
        else:
            raise ValueError("配置文件参数出错")

    # process = "sstm" #TODO 测试用
    match process:
        case "missav":
            from Spiders import missav
            missav.mainProcess()
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

if __name__ == '__main__':
    process = getargs().process
    main(process)