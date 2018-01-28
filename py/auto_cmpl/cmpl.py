import os
import config

class Cmpl():
    def __init__(self, cfg):
        self.last_build_time = None
        self.last_result = False
        self.__cfg = cfg  #config obj
        self.__cur_dir = os.getcwd()

    def compile(self):
        cmd = "build_xxx > ./result.txt"

        os.chdir(self.__cfg.get_build())
        os.system(cmd)
        print("build finish")

        os.chdir(self.__cur_dir)

    def show(self):
        print("last compile time %s"%self.last_build_time)
        print("last compile result %s"%self.last_result)
        #to show section info