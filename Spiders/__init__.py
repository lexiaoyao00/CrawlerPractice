"""各个网站的爬虫"""
from SpiderCls.driverPlaywright import ChromeDriver
from SpiderCls.mySpider import SpiderBase
from cfg import config

mcfg_yaml_parser = config.Config("yaml").get_Parser()
mcfg_ini_parser = config.Config("ini").get_Parser()

# danbooru

danbooru_rule_attrs = [
    "artist",
    "copyright",
    "characters",
    "general",
    "meta",
    "img_information",
    "post_link"
]

def sstmInitCfg():
    sstm_url = mcfg_ini_parser.get("sstm","referer")

    return sstm_url

def danbooruInitCfg():
    danbooru_url = mcfg_ini_parser.get("danbooru", "referer")
    if not danbooru_url:
        print('ini配置文件出错，"danbooru" "referer" 项有问题，请检查')
    populor_url = mcfg_ini_parser.get("danbooru", "populorUrl")
    if not populor_url:
        print('ini配置文件出错，"danbooru" "populorUrl" 键有问题，请检查')

    return danbooru_url,populor_url


def danbooruUserCfg():
    yaml_data = mcfg_yaml_parser.get_yaml()
    if yaml_data["danbooru"]:
        cfg_data = yaml_data["danbooru"]
    else:
        print('yaml配置文件出错，无 "danbooru" 键，请检查')
        raise
    
    return cfg_data

danbooru_black_list = danbooruUserCfg()["blackList"]
danbooru_url,populor_base_url = danbooruInitCfg()

sstm_url = sstmInitCfg()