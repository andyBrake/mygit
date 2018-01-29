import os
import shutil
import time
import re

#########CONFIG PROJECT PATH:set your project path####################################
PROJ_PATH = "C:\\Users\\huangfa\\workspace\\gitProject\\dualcore\\"


###############################CONSTANT###############################################
BUILD_PATH = PROJ_PATH + "build\\"
FTK_PATH = BUILD_PATH + "Image_creator\\Artemis_dual_core_firmware_package\\nvme_firmware\\"
FTK_FILE = "config_firmware_nvme_2TB_ftk.txt"

LST0_FILE = PROJ_PATH + "nvme_B0_image\\3d\\cpu0\\Artemis2_ASIC_NVME_FTL.lst"
LST1_FILE = PROJ_PATH + "nvme_B0_image\\3d\\cpu1\\Artemis2_ASIC_NVME_FTL.lst"

TEMP_FILE = BUILD_PATH + ".temp_header"
#this key variable we want to fetch from lst file, and set the relevant MACRO in map file
KEY_NAME = ['CORE_1_SAFE_CODE_DATA_SIZE', 'CORE_0_SAFE_CODE_DATA_SIZE', \
            'CORE_1_UNSAFE_CODE_DATA_SIZE', 'CORE_0_UNSAFE_CODE_DATA_SIZE', 'CORE_0_UNSAFE_INIT_SIZE']  #CORE_0_UNSAFE_INIT

#this section name in lst file
LST_NAME = ['CORE_1_SAFE_CODE_DATA' , 'CORE_0_SAFE_CODE_DATA', 'CORE_1_UNSAFE_CODE_DATA', 'CORE_0_UNSAFE_CODE_DATA', 'CORE_0_UNSAFE_INIT'] #CORE_0_INIT_CODE_SIZE

FILE_MODULE = BUILD_PATH + "temp_header_module.h" #this is the header moudle about section

######################################################################################

def get_section_info_from_lst(file, lst_ele):
    #print("in file %s to get %s."%(file, lst_ele))
    with open (file, 'r') as f :
        for line in f.readlines() :
            pattern = r'Load Region ' + lst_ele
            res = re.search(pattern, line)
            if res :
                print("get %s from:"%lst_ele)
                print(line.split(" "))
                #lst_ele_name = line.split(" ")[4]
                lst_ele_size = line.split(" ")[6].strip(',')
                return lst_ele_size
            
        return None

def get_comp_addr(files) :
    FILE_NAME_KEY = r'Execution Region '
    ADDR_KEY = r'Base: 0x[0-9,a-f]*,'

    lst_info = {}
    for lst_ele in LST_NAME:
        for file in files :
            #find one lst file
            ret = get_section_info_from_lst(file, lst_ele)
            if ret != None :
                lst_info[lst_ele] = ret
                break
            
    return lst_info

def gen_outfile(lst_info):
    with open (FILE_MODULE, 'r') as m:
        moudle_text = m.read()
        
    with open (TEMP_FILE, 'w+') as f:
        for key in lst_info:
            line = "#define " + "   " + key + "_SIZE   " + lst_info[key] + " " + r"/* for section " + key + r" */"+"\n"
            f.write(line)
        
        f.write(moudle_text)

def start() :
    lst_info = get_comp_addr([LST0_FILE, LST1_FILE])
    #generate the lst info --> lst_section_name : section_size

    print(lst_info)
    gen_outfile(lst_info)

############################################################ MAIN #######################################################
if __name__ == '__main__':
    start()


