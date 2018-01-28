import os
import shutil
import time
import re

#########CONFIG PROJECT PATH:set your project path####################################
PROJ_PATH = "C:\\Users\\huangfa\\workspace\\gitProject\\dualcore\\"
ROOT_SUB_DIR = ['boot', 'platform', 'ukrnl', 'utils']

OBJ_FILE = '''backend.c bootinfo.c cmdline.c cmdq.c common_dma.c console.c crc32.c dbg.c dma.c dtcm.c ecc.c elogspb.c
eventsrc.c exception.c fe_api.c heapalloc.c helper.c hiber.c ipc.c isr.c linearalloc.c main.c mmgr.c nanokrnl.c pdlink.c
platform.c pmu.c poolalloc.c punit.c reapMem.c reapalloc.c remap.c reqapi.c scratchpad.c sdma.c search_eng.c search_eng_test.c
serial.c sgdpool.c sgl.c spi.c state.c stkalloc.c symtab.c ukrn.c utils.c workitem.c 
'''

def extract_in_dir(dir_path):
    #print("  in %s"%dir_path)
    out_str = ""
    files = os.listdir(".\\"+ dir_path)
    for file in files :
        if ".svn" in file :
            continue
        
        if ".c" in file :
            file = os.path.join(dir_path,file) 
            out_str += file
            out_str += " "
            #print("catch %s"%file)

        sub_dir = os.path.join(dir_path,file)    
        if os.path.isdir(sub_dir) :
            #print("               digui in dir %s"%sub_dir)
            out_str += extract_in_dir(sub_dir)
        else :
            pass
            #print("%s is not a dir."%file)
    return out_str

def start() :
    out_str = ""
    os.chdir(PROJ_PATH)
    files = os.listdir(".\\")
    for file in files :
        if ".c" in file :
            out_str += file
            out_str += " "
            #print("process file %s"%file)
        if file in ROOT_SUB_DIR :
            #print("process dir in %s"%file)
            out_str += extract_in_dir(file)
    out_str = out_str.replace('\\', r'/')
    out_str = remove_unused_file(out_str, OBJ_FILE)
    
    return (out_str)

def remove_unused_file(all_file, need_obj_file):
    out = ""
    file_list = all_file.split()
    for file in file_list:
        #print(file)
        path_and_name = file.rstrip(".c")
        strinfo = re.compile(r'[a-z|A-Z]*/')
        name = strinfo.sub('',path_and_name)
        #print(name)
        if name in need_obj_file :
            #print("get %s"%file)
            out += (file + " ")
    return out.strip(" ")
    

def temp():
    os.chdir(PROJ_PATH)
    for root, dirs, files in os.walk(".\\", topdown=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))









######################################
if __name__ == '__main__':
    #temp()
    out = start()
    #print("all the c file need to compiled.")
    #for i in out.split() :
    #    print(i)

    #out = remove_unused_file(out, OBJ_FILE)
    print(out)
