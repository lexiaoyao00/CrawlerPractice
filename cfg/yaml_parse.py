import yaml
import os

class MyYAML():
    def __init__(self,filename:str):
        self.filename = filename


    def get_yaml(self):
        file_yaml = self.filename
        rf = open(file=file_yaml, mode='r', encoding='utf-8')
        crf = rf.read()
        rf.close()
        yaml_data = yaml.load(stream=crf, Loader=yaml.FullLoader)
        return yaml_data

    def dump2yaml(self,py_object,yaml_file,allow_unicode=True):
        file = open(yaml_file, 'a+', encoding='utf-8')
        yaml.dump(py_object, file,allow_unicode=allow_unicode)
        file.close()


current_file_dir = os.path.dirname(__file__)
mycfg_yaml = MyYAML(os.path.join(current_file_dir,"cfg_init.yaml"))

def testpro():
    yaml_data = mycfg_yaml.get_yaml()
    print(yaml_data)