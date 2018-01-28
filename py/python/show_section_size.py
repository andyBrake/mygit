import re
import math

#########CONFIG PROJECT PATH:set your project path####################################
PROJ_ROOT_DIR = "C:\\Users\\huangfa\\workspace\\gitProject\\dualcore\\"


#follow variable is used to compare section size change.
GIT_PRO = ""# "gitProject\\dualcore\\"
SVN_PRO = ""  #"4.5.0.64.108757\\"
TRUNK_PRO = ""#"ArtemisPlus\\Validation\\FW\\branches\\dualcore\\"

SVN_PROJ_PATH = "C:\\Users\\" + SVN_PRO  # "C:\\Users\\huangfa\\workspace\\"
GIT_PROJ_PATH = "C:\\Users\\" + GIT_PRO


#####################################################################################
BASE_FILE_NAME = "base_version.txt"
TARG_FILE_NAME = "tag_version.txt"

MEM_HEADER = PROJ_ROOT_DIR + "platform\\key_section_size.h"
#CORE_0_SAFE_CODE_DATA  in lst file size is 0, but if set 0 will meet heap error, so ignore it.
IGNOR_SECTION = ['PROGRAM_LOADI', 'SHARED_DATA', 'DATA_LOAD','PWR_UNSAFE_INIT', 'DATA_MATE', 'CORE_0_SAFE_CODE_DATA', 'PWR_SAFE_INIT']

REL_ENUM = {'DATA_LOAD':'BTCM_SIZE_0_FOR_1', 'CORE_0_SAFE_CODE_DATA':'CORE_0_SAFE_CODE_DATA_SIZE',
            'CORE_0_UNSAFE_CODE_DATA':'CORE_0_UNSAFE_CODE_DATA_SIZE', 'CORE_0_UNSAFE_INIT':'CORE_0_INIT_CODE_SIZE',
            'PWR_UNSAFE_INIT':'UNSAFE_INIT_REGION_SIZE',
            'DATA_MATE':'NIL',
            'CORE_1_SAFE_CODE_DATA':'CORE_1_SAFE_CODE_DATA_SIZE',
            'CORE_1_UNSAFE_CODE_DATA':'CORE_1_UNSAFE_CODE_DATA_SIZE',
            'CORE_1_UNSAFE_INIT':'CORE_1_INIT_CODE_SIZE',
            'PWR_SAFE_INIT':'UNSAFE_INIT_REGION_SIZE'}
######################################################################################

LST0_FILE = "build\\_out_2T_3D_0\\ASIC_NVME_FTL\\Rel\\bin\\Artemis2_ASIC_NVME_FTL.lst"
LST1_FILE = "build\\_out_2T_3D_1\\ASIC_NVME_FTL\\Rel\\bin\\Artemis2_ASIC_NVME_FTL.lst"

P1 = 'Load Region '
P2 = 'Execution Region '

def show_one_file(file_name, tag_file):
    #print(file_name)

    with open(file_name) as file:
        for line in file.readlines():
            if P1 in line :
                tag_file.write(line)
                #print(line[:-1])
            if P2 in line:
                tag_file.write("\t" + line)
                #print("\t" + line[:-1])
    return

def gen_size_file(tag_file_name, root_dir):
    lst0 = root_dir + LST0_FILE
    lst1 = root_dir + LST1_FILE

    tag_file = open(tag_file_name, "w+")

    tag_file.write("CORE 0\n")
    show_one_file(lst0, tag_file)

    tag_file.write("CORE 1\n")
    show_one_file(lst1, tag_file)

    tag_file.close()
    return

def get_size_from_line(line):
    size = 0
    res = re.search(r"Size: .*?,", line)
    if res:
        size = res.group()[6:-1]
        size = int(size, 16)
        #print("size is %d"%(size))
    return size

def get_maxsize_from_line(line):
    size = 0
    res = re.search(r"Max: .*?,", line)
    if res:
        size = res.group()[5:-1]
        size = int(size, 16)
        #print("size is %d"%(size))
    return size

def get_sec_name_from_line(line):
    name = ""
    res = re.search(r"Region .*?\(", line)
    if res:
        name = res.group()[7:-1]
        #print("size is %d"%(size))
    return name

def gen_comp_report(base_file_name, tag_file_name):
    total_change = 0
    with open(base_file_name) as base_file:
        with open(tag_file_name) as tag_file:
            lineA = base_file.readlines()
            lineB = tag_file.readlines()

            for i in range(len(lineA)):
                if "\t" in lineA[i]:
                    continue

                if "Size:" in lineA[i] or "Size:" in lineB[i]:
                    sizeA = get_size_from_line(lineA[i])
                    sizeB = get_size_from_line(lineB[i])

                    sec_nameA = get_sec_name_from_line(lineA[i])
                    sec_nameB =get_sec_name_from_line(lineB[i])

                    if sec_nameA != sec_nameB :
                        print("compare error!")
                        return

                    print("section : %s size_change : %d "%(sec_nameA, sizeB - sizeA))
                    total_change += (sizeB - sizeA)
                else :
                    pass
                    print(lineA[i][:-1])
    print("total change size %d Byte."%total_change)
    return total_change

def adjust_section_size(file_name):
    '''adjust the section size set depend on the lst file information
    '''
    global  IGNOR_SECTION
    with open(file_name) as file:
        for line in file.readlines():
            if "\t" in line:
                continue

            if 'CORE ' in line:
                print("\n" + line[:-1])
                continue

            if "Size:" in line:
                size = get_size_from_line(line)
                max_size = get_maxsize_from_line(line)
                sec_name = get_sec_name_from_line(line).strip()
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

def set_header_file():
    #set the MEM_HEADER
    pass

def start_to_adjust():
    gen_size_file(BASE_FILE_NAME, PROJ_ROOT_DIR)

    adjust_section_size(BASE_FILE_NAME)
    return 0

def start():
    comp_base_version = GIT_PROJ_PATH
    comp_tag_version  = SVN_PROJ_PATH

    gen_size_file(BASE_FILE_NAME, comp_base_version)
    gen_size_file(TARG_FILE_NAME,  comp_tag_version)

    gen_comp_report(BASE_FILE_NAME, TARG_FILE_NAME)







############################################################ MAIN #######################################################
if __name__ == '__main__':
    #start()
    start_to_adjust()
