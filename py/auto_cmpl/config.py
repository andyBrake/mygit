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
        self.__lst_filename = "Artemis2_ASIC_NVME_FTL.lst"
        self.__ftk = self.__build + "Image_creator\\Artemis_dual_core_firmware_package\\nvme_firmware\\"
        #temp output dir
        self.out_dir = [self.__build + '_out_2T_3D_0', self.__build + '_out_2T_3D_1', self.__build + '_out_2T_2D_0', self.__build + '_out_2T_2D_1',
                self.__build + "_feedback"]

        if raid:
            self.__image = self.__root + "nvme_B0_image_raid\\"
            self.__ftk_filename = "config_firmware_nvme_2TB_raid_ftk.txt"
        else:
            self.__image = self.__root + "nvme_B0_image\\"
            self.__ftk_filename = "config_firmware_nvme_2TB_ftk.txt"

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

    def get_lst_file_name(self):
        return self.__lst_filename

    def get_lst0_file(self):
        return self.__bin0 + self.__lst_filename

    def get_lst1_file(self):
        return self.__bin1 + self.__lst_filename

    def get_ftk_file(self):
        return self.__ftk + self.__ftk_filename

    def show(self):
        print("show config info:")
        print("\tproject name %s"%(self.__name))
        print("\troot path %s"%(self.__root))
        print("\tsupport raid %s "%(self.__raid))
        print("\tsupport burner %s"%(self.__burner))
        print("\tbuild path %s"%self.__build)
        print("\timage path %s"%self.__image)
        print("\tbin0 path %s"%self.__bin0)
        print("\tbin1 path %s"%self.__bin1)
        print("config info end\n")

