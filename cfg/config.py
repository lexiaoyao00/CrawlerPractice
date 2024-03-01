from .ini_parse import mycfg_ini
from .yaml_parse import mycfg_yaml

class Config():
    def __init__(self,config_extension:str):
        self.config = config_extension

    def get_Parser(self):
        obj = self.config

        if obj == "ini":
            self.cfg_parser = mycfg_ini
        elif obj == "yaml":
            self.cfg_parser = mycfg_yaml


        else:
            self.cfg_parser = None
            print("当前配置文件无对象")

        return self.cfg_parser