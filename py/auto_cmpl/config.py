import xml_utils

class Config():

    def __init__(self, name, root_path, raid=True, burner=True):
        self.__name = name #string
        self.__root = root_path #string
        self.__raid = raid      #bool
        self.__burner = burner  #bool

        self.__build = self.__root + "\\build\\"
        if raid:
            self.__image = self.__root + "image" + "_raid\\"
        else:
            self.__image = self.__root + "image" + "\\"


    def get_root(self):
        return self.__root

    def get_build(self):
        return self.__build

    def show(self):
        print("project name %s"%(self.__name))
        print("root path %s"%(self.__root))
        print("support raid %s "%(self.__raid))
        print("support burner %s"%(self.__burner))
        print("build path %s"%self.__build)
        print("image path %s"%self.__image)

