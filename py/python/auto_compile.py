import os
import shutil
import time

# temp compile path, for test git project code
raid = True
test = False
TEMP_PATH = "C:\\Users\\huangfa\\workspace\\gitProject\\dualcore\\build"

#if you compile version FW, set test = FALSE, and use the followed path.
VERSION = "4.5.0.60.108341" #4.5.0.56.108251
COMP_PATH = "C:\\Users\\huangfa\\workspace\\"+ VERSION + "\\build"

#the path stored your all history FW, and will be fired into device
FIRED_PATH = "C:\\Users\\huangfa\\workspace\\firmware_version\\fireinto\\FW\\nvme_B0_image"
#below path based on COMP_PATH
BIN_PATH0 = ".\\_out_2T_3D_0\\ASIC_NVME_FTL\\Rel\\bin"
BIN_PATH1 = ".\\_out_2T_3D_1\\ASIC_NVME_FTL\\Rel\\bin"

if raid:
    IMAGE_PATH = "..\\nvme_B0_image_raid"
else:
    IMAGE_PATH = "..\\nvme_B0_image"


BUILD_CMD = "build_nvme_B0_2TB_FW.bat "
BUILD_RESULT= " > ../build_result.txt"
####################################################### FUNCTION ######################################################

def filter_comp_result() :
    warning0 = 'Warning: C9931W:'
    warning1 = 'Warning: A9931W:'
    warning2 = 'Warning: L9931W:'
    with open('../build_result.txt', 'r') as f:
        with open('../fitered_result.txt', 'w') as g:
            for line in f.readlines():
                if warning0 not in line and warning1 not in line and warning2 not in line :             
                    g.write(line)

def rm_old_image(path):
    os.chdir(path)
    #print("rm old file in %s. \n"%(COMP_PATH))
    if os.path.exists(BIN_PATH0) :
        os.chdir(BIN_PATH0)
        delAllFiles()
        
    os.chdir(path)
    if os.path.exists(BIN_PATH1) :
        os.chdir(BIN_PATH1)
        delAllFiles()

#delete all files in current path
def delAllFiles():
    files = os.listdir(".\\")
    for file in files :
        os.remove(file)
    print("del all file in %s."%(os.getcwd()))


def bak_and_copy_bin_file():
    #print("bak old file in %s. \n"%(COMP_PATH))
    if raid :
        bin_file = "image_package_3d_tlc_7op_raid.bin"
    else :
        bin_file = "image_package_3d_tlc_7op.bin"

    #bakup the old bin file
    os.chdir(FIRED_PATH)
    if os.path.exists(bin_file) :
        date = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
        shutil.copy(".\\" + bin_file, ".\\bak_"+date+".bin")
        print("backup pre fired image in %s"%(date))
        
    else :
        print("no pre image need to backup.")
    #copy the new bin to fire path
    os.chdir(COMP_PATH)
    os.chdir(IMAGE_PATH)
    shutil.copy(".\\" + bin_file, FIRED_PATH)


def check_compile_result() :
    #print("check result in %s. \n"%(COMP_PATH))

    if raid:
        bin_file = "image_package_3d_tlc_7op_raid.bin"
    else :
        bin_file = "image_package_3d_tlc_7op.bin"
    
    os.chdir(COMP_PATH)
    os.chdir(BIN_PATH0)
    if not os.path.exists("Artemis2_ASIC_NVME_FTL_0.axf") :
        print("CPU0 file not created.")
        return 1

    os.chdir(COMP_PATH)
    os.chdir(BIN_PATH1)
    if not os.path.exists("Artemis2_ASIC_NVME_FTL_1.axf") :
        print("CPU1 file not created.")
        return 1

    os.chdir(COMP_PATH)
    os.chdir(IMAGE_PATH)
    if not os.path.exists(bin_file):
        print("image file not created.")
        return 1

    return 0

def start():
    global BUILD_CMD

    print("\n-------------start to generate image-----\n\tdir : "+COMP_PATH+"\n------------------------------------------------")
    print(time.strftime("%Y-%m-%d-%H:%M:%S\n", time.localtime()))
    
    start_clk = time.clock()

    #remove old image
    rm_old_image(COMP_PATH)
    print("remove old axf file success!\n")

    #build
    os.chdir(COMP_PATH)
    os.system("python build_clean.py")

    print("build in %s."%(os.getcwd()))
    if raid :
        BUILD_CMD = BUILD_CMD + " raid"

    print("build cmd: %s."%(BUILD_CMD + BUILD_RESULT))
    os.system(BUILD_CMD + BUILD_RESULT)
    print("build finish!\n")

    filter_comp_result()

    #check is all bin file be created
    ret = check_compile_result()
    if 0 != ret :
        start_clk = time.clock() - start_clk
        print("compile error, use sec %f"%start_clk)
        return 1

    print("generate the image file success!\n")

    #backup old bin file in firedir and copy the new bin file to firepath
    if not test :
        bak_and_copy_bin_file()


    print("Finish %s!\n"%(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))
    start_clk = time.clock() - start_clk
    print("use sec %f"%start_clk)
    return 0


def build_clean():
    os.chdir(COMP_PATH)
    os.system("python build_clean.py")
    return 0

############################################################ MAIN #######################################################
if __name__ == '__main__':
    # if test:
    #     COMP_PATH = TEMP_PATH  #only for test git code
    #     print("\nbuild the git code, just test code.")
    COMP_PATH = TEMP_PATH #use the git project to build
    #build_clean();
    start()
