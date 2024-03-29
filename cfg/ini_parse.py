from configparser import ConfigParser
import os

class CfgOperation:
    def __init__(self,path:str):
        self._path = path
        self._parser = ConfigParser()
        self._parser.read(self._path,encoding='utf-8')

    @property
    def parser(self):
        return self._parser

    def get(self,section,option):
        return self._parser.get(section,option)

    def getInitCfg(self):
        return self._parser.items('initCfg')

    def get_keys(self,section:str):
        return self._parser.options(section)

    def has_section(self,section):
        return self._parser.has_section(section)



    def save(self,filename:str):
        self._parser.write(open(filename, 'a',encoding='utf-8'))\

current_file_dir = os.path.dirname(__file__)
mycfg_ini = CfgOperation(os.path.join(current_file_dir,"cfg_init.ini"))