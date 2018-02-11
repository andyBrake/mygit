import os
import time
import shutil
import re
import math

class Cmpl():
    def __init__(self, cfg):
        self.last_build_time = "no build"
        self.last_result = False
        self.__cfg = cfg  # config obj
        self.__cur_dir = os.getcwd()
        #the section size info files
        self.base_file_name = "base_version.txt"

    def compile(self):
        self.__cfg.show()
        os.chdir(self.__cfg.get_root())

        print(
            "\n-------------start to generate image--------------------------\n"
            "\tdir : " + os.getcwd() +
            "\n--------------------------------------------------------------")
        print(time.strftime("\tbuild start time: %Y-%m-%d-%H:%M:%S", time.localtime()))
        print("--------------------------------------------------------------")

        start_clk = time.clock()

        # remove old image
        self.__rm_old_image()
        print("remove old axf file success!\n")
        os.chdir(self.__cfg.get_build())
        os.system("python build_clean.py")

        # build


        if self.__cfg.get_raid():
            cmd = cmd = "build_nvme_B0_2TB_FW.bat raid > ../build_result.txt"
        else:
            cmd = "build_nvme_B0_2TB_FW.bat > ../build_result.txt"
        print("start to build, please wait...!")
        os.chdir(self.__cfg.get_build())
        os.system(cmd)
        print("build finish!\n")
        self.last_build_time = time.strftime("finish time: %Y-%m-%d-%H:%M:%S\n", time.localtime())

        self.__filter_comp_result()

        # check is all bin file be created
        ret = self.__check_compile_result()
        if not ret:
            start_clk = time.clock() - start_clk
            print("compile error, use sec %f" % start_clk)
            self.last_result = False
            return 1

        self.last_result = True
        print("generate the image file success!\n")

        # backup old bin file in firedir and copy the new bin file to firepath
        if self.__cfg.get_firepath():
            self.__bak_and_copy_bin_file()

        print("this build %s" % (self.last_build_time))
        start_clk = time.clock() - start_clk
        print("use second %f" % start_clk)

        os.chdir(self.__cur_dir)
        return

    def build_ok(self):
        return self.last_result

    def show(self):
        print("last compile time %s" % (self.last_build_time))#
        print("last compile result %s" % self.last_result)
        # to show section info

    def __filter_comp_result(self):
        warnings = ['Warning: C9931W:', 'Warning: A9931W:', 'Warning: L9931W:', 'Warning: C9560I:', 'Warning: C4052E:' ]

        os.chdir(self.__cfg.get_build())
        with open('../build_result.txt', 'r') as f:
            with open('../fitered_result.txt', 'w') as g:
                for line in f.readlines():
                    ignore = False
                    for warn in warnings:
                        if warn in line:
                            ignore = True
                            break
                    if not ignore:
                        g.write(line)

        os.chdir(self.__cur_dir)
        return

    def __rm_old_image(self):
        # print("rm old file in %s. \n"%(COMP_PATH))
        #path = os.getcwd()
        if os.path.exists(self.__cfg.get_bin0()):
            os.chdir(self.__cfg.get_bin0())
            self.__delAllFiles()

        #os.chdir(path)
        if os.path.exists(self.__cfg.get_bin1()):
            os.chdir(self.__cfg.get_bin1())
            self.__delAllFiles()

        #os.chdir(path)
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

        try:
            os.chdir(self.__cfg.get_bin0())
        except Exception:
            print("the dir %s is not genearated.build may fail."%self.__cfg.get_bin0())
            return  False

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

    #clean all the build output
    def build_clean(self):
        FW_PAC_DIR = self.__cfg.get_build() +'Image_creator\\Artemis_dual_core_firmware_package\\'
        #some output  files must removed
        TMP_IMAGE_FILE_LIST = [FW_PAC_DIR + "image_firmware.bin", FW_PAC_DIR + "misc_cfg.bin"]
        TMP_SEC_FILE_LIST = ["image_firmware.bin", "C0_ATCM_0", "C0_BTCM", "C0_SDATA",
                         "C0_UNSAFE_CODE_DATA", "C1_ATCM", "C1_BTCM", "C1_INIT_CODE_BASE",
                         "C1_PS_CODE", "C1_UNSAFE_CODE_DATA", "INIT_CODE_BASE",
                         "SDATA", "SLOW_DATA", "Artemis2_ASIC_NVME_FTL.lst",
                         "Artemis2_ASIC_NVME_FTL_0.axf", "Artemis2_ASIC_NVME_FTL_1.axf"]

        os.chdir(self.__cfg.get_root())

        try :
            shutil.rmtree(self.__cfg.get_image())
        except Exception:
            pass

        for each_dir in self.__cfg.out_dir:
            try :
                shutil.rmtree(each_dir)
            except Exception:
                pass

        for each_file in TMP_IMAGE_FILE_LIST:
            if os.path.exists(each_file):
                os.system("del " + each_file)

        for section_file in TMP_SEC_FILE_LIST:
            del_file = FW_PAC_DIR + "nvme_firmware\\" + section_file
            if os.path.exists(del_file):
                os.system("del " + del_file)

        print("clean all build files OK.")
        os.chdir(self.__cur_dir)
        return

    #calc the right section size for each segment
    def start_to_adjust(self):
        ret = self.gen_size_file(self.base_file_name)
        if ret != 0:
            return 1

        self.adjust_section_size(self.base_file_name)
        return 0

    def gen_size_file(self, tag_file_name):
        lst0 = self.__cfg.get_bin0() + self.__cfg.get_lst_file_name()
        lst1 = self.__cfg.get_bin1() + self.__cfg.get_lst_file_name()

        if (not os.path.exists(lst0)) or (not os.path.exists(lst1)) :
            print("lst file not generate, compile may meet error.")
            return 1

        tag_file = open(tag_file_name, "w+")

        tag_file.write("CORE 0\n")
        self.__rec_one_file(lst0, tag_file)

        tag_file.write("CORE 1\n")
        self.__rec_one_file(lst1, tag_file)

        tag_file.close()
        return 0

    def __rec_one_file(self, file_name, tag_file):
        P1 = 'Load Region '
        P2 = 'Execution Region '

        with open(file_name) as file:
            for line in file.readlines():
                if P1 in line :
                    tag_file.write(line)
                    #print(line[:-1])
                if P2 in line:
                    tag_file.write("\t" + line)
                    #print("\t" + line[:-1])
        return

    #decide each section size
    def adjust_section_size(self, file_name):
        '''adjust the section size set depend on the lst file information
        '''
        IGNOR_SECTION = ['PROGRAM_LOADI', 'SHARED_DATA', 'DATA_LOAD','PWR_UNSAFE_INIT', 'DATA_MATE', 'CORE_0_SAFE_CODE_DATA', 'PWR_SAFE_INIT']
        REL_ENUM = {'DATA_LOAD':'BTCM_SIZE_0_FOR_1', 'CORE_0_SAFE_CODE_DATA':'CORE_0_SAFE_CODE_DATA_SIZE',
            'CORE_0_UNSAFE_CODE_DATA':'CORE_0_UNSAFE_CODE_DATA_SIZE', 'CORE_0_UNSAFE_INIT':'CORE_0_INIT_CODE_SIZE',
            'PWR_UNSAFE_INIT':'UNSAFE_INIT_REGION_SIZE',
            'DATA_MATE':'NIL',
            'CORE_1_SAFE_CODE_DATA':'CORE_1_SAFE_CODE_DATA_SIZE',
            'CORE_1_UNSAFE_CODE_DATA':'CORE_1_UNSAFE_CODE_DATA_SIZE',
            'CORE_1_UNSAFE_INIT':'CORE_1_INIT_CODE_SIZE',
            'PWR_SAFE_INIT':'UNSAFE_INIT_REGION_SIZE'}

        with open(file_name) as file:
            for line in file.readlines():
                if "\t" in line:
                    continue

                if 'CORE ' in line:
                    print("\n" + line[:-1])
                    continue

                if "Size:" in line:
                    size = self.get_size_from_line(line)
                    max_size = self.get_maxsize_from_line(line)
                    sec_name = self.get_sec_name_from_line(line).strip()
                    new_size = math.ceil(size/32) * 32
                    try :
                        sec_enum = REL_ENUM[sec_name]
                    except Exception:
                        sec_enum = 'NIL'

                    #print("%d %d"%(size, new_size))
                    #new_size = int((int((size - 1)/32) + 1)*32)

                    #each section size must align with 32 Byte
                    if max_size%32 != 0:
                        print("section : %s max_size %d is not align with 32 Byte, must set %s %d. "%(sec_name, max_size, sec_enum, math.ceil(max_size/32) * 32))
                        continue

                    if sec_name in IGNOR_SECTION:
                        print("ignore %s"%sec_name)
                        continue

                    if max_size == new_size:
                        print("section : %s match.max_size %d, new_size %d.Don't need to modify enum %s "%(sec_name,max_size, new_size, sec_enum))
                        continue
                    elif max_size > new_size:
                        #pass
                        print("section %s need to decrease size(%d, %d)."%(sec_name, max_size, size))
                    else:
                        #pass
                        print("section %s need to increase size(%d, %d)."%(sec_name, max_size, size))
                    #if max_size != size:
                    #    print("%d %d %d"%(max_size, new_size, max_size - new_size))
                    print("\tsection : %s old max size : %d[%s], new max size : %d[%s] "%(sec_name,max_size,hex(max_size), new_size, hex(new_size)))
                    print("\tset %s %d." %(sec_enum, new_size))

                else :
                    pass
        return 0


    def get_size_from_line(self, line):
        size = 0
        res = re.search(r"Size: .*?,", line)
        if res:
            size = res.group()[6:-1]
            size = int(size, 16)
            #print("size is %d"%(size))
        return size

    def get_maxsize_from_line(self, line):
        size = 0
        res = re.search(r"Max: .*?,", line)
        if res:
            size = res.group()[5:-1]
            size = int(size, 16)
            #print("size is %d"%(size))
        return size

    def get_sec_name_from_line(self, line):
        name = ""
        res = re.search(r"Region .*?\(", line)
        if res:
            name = res.group()[7:-1]
            #print("size is %d"%(size))
        return name

    #modify ftk file to match each section size in lst file
    def fix_addr2ftk(self) :
        seg_info = self.__get_section_addr_from_ftkfile()
        new_info = self.__get_section_addr_from_lstfile(seg_info)
        self.__write_filename_addr(self.__cfg.get_ftk_file(), seg_info, new_info)
        return

    #read the ftk file, and return each section {name:addr}
    def __get_section_addr_from_ftkfile(self) :
        STR_FILE_NAME = "FILE_NAME"
        STR_LOAD_ADDRESS = "LOAD_ADDRESS"
        file = self.__cfg.get_ftk_file()
        seg_info_table = {} #seg_info_table is a dictionary of FILE_NAME : LOAD_ADDRESS

        with open(file, 'r') as f:
            file_name = []
            addr = []
            for line in f.readlines():
                if STR_FILE_NAME in line :
                    file_name = line[12:-1]
                if STR_LOAD_ADDRESS in line :
                    addr = line[15:-1]
                    #print("file_name : [%s]  addr : [%s]" %(file_name, addr))
                    seg_info_table[file_name] = addr
        return seg_info_table

    #read the lst0 and lst1 file, set each section new addr, and return as new_info_table dic
    def __get_section_addr_from_lstfile(self, seg_info_table) :
        FILE_NAME_KEY = r'Execution Region '
        ADDR_KEY = r'Base: 0x[0-9,a-f]*,'

        lst0_file = self.__cfg.get_lst0_file()
        lst1_file = self.__cfg.get_lst1_file()
        new_info_table = {}

        with open(lst0_file, 'r') as f0 :
            lines0 = f0.readlines()
            with open(lst1_file, 'r') as f1 :
                lines1 = f1.readlines()

                for file_name in seg_info_table :
                    #print("want to find file name : [%s]"%file_name)
                    res = None
                    addr = ''
                    #search file_name in files0
                    for line in lines0 :
                        #print("find in %s"%line)
                        res = re.search(FILE_NAME_KEY + file_name, line,re.M|re.I)
                        if res:
                            #print(line)
                            mat = re.search(ADDR_KEY, line)
                            addr = mat.group()[6:-1]
                            #print("[%s:%s]\n"%(file_name,addr))
                            new_info_table[file_name] = addr
                            break
                    #in lst0 found, no need to search in lst1
                    if res :
                        continue

                    #search file_name in files1
                    for line in lines1 :
                        #print("find in %s"%line)
                        res = re.search(FILE_NAME_KEY + file_name, line,re.M|re.I)
                        if res:
                            #print(line)
                            mat = re.search(ADDR_KEY, line)
                            addr = mat.group()[6:-1]
                            #print("[%s:%s]\n"%(file_name,addr))
                            new_info_table[file_name] = addr
                            break
        return new_info_table

    def __write_filename_addr(self, file, seg_info_table, new_seg_info_table):
        KEY_NAME = ['C0_BTCM','C0_UNSAFE_CODE_DATA', 'INIT_CODE_BASE', 'C1_UNSAFE_CODE_DATA', 'C1_INIT_CODE_BASE']
        STR_FILE_NAME = "FILE_NAME"
        STR_LOAD_ADDRESS = "LOAD_ADDRESS"
        bak_file = file+".bak"

        misMatch = False
        for key in seg_info_table :
            #print("key %s, old addr [%s], new addr [%s]"%(key, seg_info[key], new_info[key]))
            if (key in KEY_NAME) and (seg_info_table[key] != new_seg_info_table[key]) :
                print("\tunmatch-key %s %s %s"%(key, seg_info_table[key], new_seg_info_table[key]))
                misMatch = True
                break

        if not misMatch:
            print("ftk file is correct, no need modify.")
            return

        with open(file, 'r') as f:
            with open(bak_file, 'w+') as g:
                file_name = []
                addr = []
                for line in f.readlines():
                    if STR_FILE_NAME in line :
                        file_name = line[12:-1]
                        addr = new_seg_info_table[file_name]

                    if STR_LOAD_ADDRESS in line :
                        if  file_name in KEY_NAME :
                            g.write(STR_LOAD_ADDRESS + ' = ' + addr + '\n')
                            print("change [%s] addr[%s] to [%s]"%(file_name, line[15:-1],addr))
                            continue
                    g.write(line)

        #shutil.copy(file, file + ".tempfile")
        shutil.copy(bak_file, file)
        #shutil.copy(file + ".tempfile", file)
        #os.system("del " + file + ".tempfile")
        os.system("del " + bak_file)
        return