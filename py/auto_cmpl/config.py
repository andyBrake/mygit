import xml_utils

class Config():

    def __init__(self, name, root_path, raid=True, burner=True, firepath = None):
        self.__name = name #string
        self.__root = root_path #string
        self.__raid = raid      #bool
        self.__burner = burner  #bool
        self.__firepath = firepath

        self.__build = self.__root + "build\\"
        self.__bin0 = self.__build + "_out_2T_3D_0\\ASIC_NVME_FTL\\Rel\\bin\\"
        self.__bin1 = self.__build + "_out_2T_3D_1\\ASIC_NVME_FTL\\Rel\\bin\\"
        if raid:
            self.__image = self.__root + "nvme_B0_image_raid\\"
        else:
            self.__image = self.__root + "nvme_B0_image\\"

    def get_root(self):
        return self.__root

    def get_build(self):
        return self.__build

    def get_raid(self):
        return self.__raid

    def get_firepath(self):
        return self.__firepath

    def get_image(self):
        return self.__image

    def get_bin0(self):
        return self.__bin0

    def get_bin1(self):
        return self.__bin1

    def show(self):
        print("project name %s"%(self.__name))
        print("root path %s"%(self.__root))
        print("support raid %s "%(self.__raid))
        print("support burner %s"%(self.__burner))
        print("build path %s"%self.__build)
        print("image path %s"%self.__image)
        print("bin0 path %s"%self.__bin0)
        print("bin1 path %s"%self.__bin1)

