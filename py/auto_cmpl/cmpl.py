import os
import time
import config

class Cmpl():
    def __init__(self, cfg):
        self.last_build_time = None
        self.last_result = False
        self.__cfg = cfg  # config obj
        self.__cur_dir = os.getcwd()

    def compile(self):

        self.__cfg.show()
        os.chdir(self.__cfg.get_root())

        print(
            "\n-------------start to generate image-----\n"
            "\tdir : " + os.getcwd() +
            "\n------------------------------------------------")
        print(time.strftime("%Y-%m-%d-%H:%M:%S\n", time.localtime()))

        start_clk = time.clock()

        # remove old image
        self.__rm_old_image()
        print("remove old axf file success!\n")

        # build
        os.chdir(self.__cfg.get_build())
        os.system("python build_clean.py")

        if self.__cfg.get_raid():
            cmd = cmd = "build_nvme_B0_2TB_FW.bat raid > ./build_result.txt"
        else:
            cmd = "build_nvme_B0_2TB_FW.bat > ./build_result.txt"
        os.system(cmd)
        print("build finish!\n")

        self.__filter_comp_result()

        # check is all bin file be created
        ret = self.__check_compile_result()
        if not ret:
            start_clk = time.clock() - start_clk
            print("compile error, use sec %f" % start_clk)
            return 1

        print("generate the image file success!\n")

        # backup old bin file in firedir and copy the new bin file to firepath
        if self.__cfg.get_firepath():
            self.__bak_and_copy_bin_file()

        print("Finish %s!\n" % (time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))
        start_clk = time.clock() - start_clk
        print("use sec %f" % start_clk)

        os.chdir(self.__cur_dir)
        return

    def show(self):
        print("last compile time %s" % self.last_build_time)
        print("last compile result %s" % self.last_result)
        # to show section info

    def __filter_comp_result(self):
        warning0 = 'Warning: C9931W:'
        warning1 = 'Warning: A9931W:'
        warning2 = 'Warning: L9931W:'

        os.chdir(self.__cfg.get_build())
        with open('../build_result.txt', 'r') as f:
            with open('../fitered_result.txt', 'w') as g:
                for line in f.readlines():
                    if warning0 not in line and warning1 not in line and warning2 not in line:
                        g.write(line)
        os.chdir(self.__cur_dir)
        return

    def __rm_old_image(self):
        # print("rm old file in %s. \n"%(COMP_PATH))
        path = os.getcwd()
        if os.path.exists(self.__cfg.get_bin0()):
            os.chdir(self.__cfg.get_bin0())
            self.__delAllFiles()

        os.chdir(path)
        if os.path.exists(self.__cfg.get_bin1()):
            os.chdir(self.__cfg.get_bin1())
            self.__delAllFiles()

        os.chdir(path)
        return

    # delete all files in current path
    def __delAllFiles(self):
        files = os.listdir(".\\")
        for file in files:
            os.remove(file)
        return

    def __bak_and_copy_bin_file(self):
        # print("bak old file in %s. \n"%(COMP_PATH))
        if self.__cfg.get_raid():
            bin_file = "image_package_3d_tlc_7op_raid.bin"
        else:
            bin_file = "image_package_3d_tlc_7op.bin"

        # bakup the old bin file
        firepath = self.__cfg.get_firepath()
        if firepath:
            os.chdir(firepath)
            if os.path.exists(bin_file):
                date = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
                shutil.copy(".\\" + bin_file, ".\\bak_" + date + ".bin")
                print("backup pre fired image in %s" % (date))
            else:
                print("no pre image need to backup.")

            os.chdir(self.__cfg.get_image())
            shutil.copy(".\\" + bin_file, firepath)
        else:
            print("no need to fire fw.")
        # copy the new bin to fire path
        return

    def __check_compile_result(self):
        # print("check result in %s. \n"%(COMP_PATH))
        if self.__cfg.get_raid():
            bin_file = "image_package_3d_tlc_7op_raid.bin"
        else:
            bin_file = "image_package_3d_tlc_7op.bin"

        os.chdir(self.__cfg.get_bin0())
        if not os.path.exists("Artemis2_ASIC_NVME_FTL_0.axf"):
            print("CPU0 file not created.")
            return False
        os.chdir(self.__cfg.get_bin1())
        if not os.path.exists("Artemis2_ASIC_NVME_FTL_1.axf"):
            print("CPU1 file not created.")
            return False

        os.chdir(self.__cfg.get_image())
        if not os.path.exists(bin_file):
            print("image file not created.")
            return False
        return True

    def build_clean(self):
        os.chdir(self.__cfg.get_build())
        os.system("python build_clean.py")
        os.chdir(self.__cur_dir)
        return
