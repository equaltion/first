import json
import os
from contextlib import contextmanager
#负责监管各项设置的json的类，理应可以避免依赖于其他的文件，被main调用之后通过核心类运行
class config:
    #初始化，获得或建立设置文件和回调函数
    def __init__(self,config_file_path,callback=None,save_path=None):
        #首先需要知道config.json在哪
        self.config_file_path=config_file_path
        self.callback=callback
        self.save_path=save_path
        self.data_dict={}

        #用类里面的读取函数尝试打开这个文件,
        self.load(self.config_file_path)
        self.org_data_dict=self.data_dict
    #重定向，更改设置文件
    def reload(self,file_path):
        self.load(self,file_path)
        self.config_file_path=file_path

    #读取函数
    def load(self,file_path):
        self.check(self,file_path)
        with open(file_path,'r',encoding='utf-8') as file:
            self.data_dict=json.load(file)
        
        

    #自检，检验文件是否存在
    def check(self,file_path,_encoding='utf-8'):
        self.callback(f"try_open:{file_path}")
        try:
            #直接打开，让open告诉我们发生了什么
            with open(file_path,'r+',encoding=_encoding) as file:
                pass
        except FileNotFoundError:
            #找不到文件，即os.path.exists(self.config_file)==false
            raise
        except IsADirectoryError:
            #给出的路径是目录而非文件，即os.path.isfile(self.config_file)==false
            raise 
        except PermissionError:
            #没有权限读取，即os.access(self.config_file)==false
            raise 
        except UnicodeDecodeError:
            raise 
        except json.JSONDecodeError :
            raise 
        except OSError :
            raise 

    #临时回调函数调整
    @contextmanager
    def temp_config_callback(self,new_callback):
        temp=self.callback
        self.callback=new_callback
        try:
            yield
        finally:
            self.callback=temp

    def save(self,save_path=None):

        if  save_path is not None:
            target =save_path
        elif  self.save_path is not None:
            target=self.save_path
        else:
             self.callback('save_loss:not_path_for_save')
        self.check(target)
        with open(target,'w',encoding='utf-8') as file:
            json.dump(self.data_dict,file,indent=2)


    def dumps(self):
        return json.dumps(self.data_dict,indent=2)

    def get(self,key):
        return self.data_dict.get(key,None)

    def set_value(self, key, value, auto_save=True):
        self.data_dict[key] = value
        if auto_save:
            self.save()

    def set_dict(self, new_dict,auto_save=True):
        for key, value in new_dict.items():
            self.data_dict[key] = value
        if auto_save:
            self.save()

    def set(self,*,auto_save=True,**kwargs):
            self.set_dict(kwargs,auto_save)
    #今天的代码就写到这里吧~