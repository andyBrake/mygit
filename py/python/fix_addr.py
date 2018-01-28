import os
import shutil
import re

#########CONFIG PROJECT PATH:set your project path####################################
PROJ_PATH = "C:\\Users\\huangfa\\workspace\\gitProject\\dualcore\\"
RAID = ""#"_raid"

######################################################################################
BUILD_PATH = PROJ_PATH + "build\\"
FTK_PATH = BUILD_PATH + "Image_creator\\Artemis_dual_core_firmware_package\\nvme_firmware\\"
FTK_FILE = "config_firmware_nvme_2TB" + RAID +  "_ftk.txt"

LST0_FILE = PROJ_PATH + "nvme_B0_image" + RAID + "\\3d" + RAID + "\\cpu0\\Artemis2_ASIC_NVME_FTL.lst"
LST1_FILE = PROJ_PATH + "nvme_B0_image" + RAID + "\\3d" + RAID + "\\cpu1\\Artemis2_ASIC_NVME_FTL.lst"

FILE_NAME = 0
LOAD_ADDRESS = 1

key_name = ['C0_BTCM','C0_UNSAFE_CODE_DATA', 'INIT_CODE_BASE', 'C1_UNSAFE_CODE_DATA', 'C1_INIT_CODE_BASE']

#read the ftk file, and return each section {name:addr}
def get_seg_info(file) :
    STR_FILE_NAME = "FILE_NAME"
    STR_LOAD_ADDRESS = "LOAD_ADDRESS"
    seg_info_table = {} #seg_info_table is a dictionary of FILE_NAME : LOAD_ADDRESS
    
    with open(file, 'r') as f:
        file_name = []
        addr = []
        for line in f.readlines():
            if STR_FILE_NAME in line :             
                file_name = line[12:-1]
            if STR_LOAD_ADDRESS in line :
                addr = line[15:-1]
                print("file_name : [%s]  addr : [%s]" %(file_name, addr))
                seg_info_table[file_name] = addr
    return seg_info_table

#read the lst0 and lst1 file, set each section new addr, and return as new_info_table dic
def get_comp_addr(files, seg_info_table, new_info_table) :
    FILE_NAME_KEY = r'Execution Region '
    ADDR_KEY = r'Base: 0x[0-9,a-f]*,'
    
    with open(files[0], 'r') as f0 :
        lines0 = f0.readlines()
        with open(files[1], 'r') as f1 :
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
    return
                
def write_filename_addr(file, seg_info_table):
    STR_FILE_NAME = "FILE_NAME"
    STR_LOAD_ADDRESS = "LOAD_ADDRESS"
    bak_file = file+".bak"
    with open(file, 'r') as f:
        with open(bak_file, 'w+') as g:
            file_name = []
            addr = []
            for line in f.readlines():
                if STR_FILE_NAME in line :             
                    file_name = line[12:-1]
                    addr = seg_info_table[file_name]
                    
                if STR_LOAD_ADDRESS in line :
                    if  file_name in key_name :  
                        g.write(STR_LOAD_ADDRESS + ' = ' + addr + '\n')
                        print("change [%s] addr[%s] to [%s]"%(file_name, line[15:-1],addr))
                        continue
                g.write(line)

    #shutil.copy(file, file + ".tempfile")
    shutil.copy(bak_file, file)
    #shutil.copy(file + ".tempfile", file)
    #os.system("del " + file + ".tempfile")
    os.system("del " + bak_file)

    print("modify %s success."%(file))
    return
                
def start() :
    file = FTK_PATH + FTK_FILE
    seg_info = get_seg_info(file)
    new_info = {}
                
    get_comp_addr([LST0_FILE, LST1_FILE], seg_info, new_info)

    #test is there some section addr need to modify
    misMatch = False
    for key in seg_info :
        #print("key %s, old addr [%s], new addr [%s]"%(key, seg_info[key], new_info[key]))
        if seg_info[key] != new_info[key] :
            #print("\tunmatch-key %s"%key)
            misMatch = True
    #if need modify, write the new addr to a bak file
    if misMatch :
        #write the new addr to ftk file
        print("write")
        write_filename_addr(file, new_info)
    

############################################################ MAIN #######################################################
if __name__ == '__main__':
    start()

