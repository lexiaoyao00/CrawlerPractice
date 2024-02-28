from .ini_parse import mycfg_ini
from .yaml_parse import mycfg_yaml

class Config():
    def __init__(self,config_extension:str):
        self.config = config_extension

    def get_config(self,config_extension:str|None = None):
        obj = config_extension if config_extension else self.config

        if obj == "ini":
            self.cfg_obj = mycfg_ini
        elif obj == "yaml":
            self.cfg_obj = mycfg_yaml


        else:
            self.cfg_obj = None
            print("当前配置文件无对象")

        return self.cfg_obj