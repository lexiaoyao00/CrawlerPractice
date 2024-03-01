"""各个网站的爬虫"""
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
    "img_information"
]
def danbooruCfg():
    yaml_data = mcfg_yaml_parser.get_yaml()
    if yaml_data["danbooru"]:
        cfg_data = yaml_data["danbooru"]
    else:
        print('yaml配置文件出错，无 "danbooru" 键，请检查')
        raise
    
    return cfg_data

danbooru_black_list = danbooruCfg()["blackList"]