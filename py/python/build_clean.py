import os
import sys
import shutil

BUILD_DIR = ".\\"
IMAGE_DIR = BUILD_DIR + '..\\nvme_B0_image\\'
IMAGE_RAID_DIR = BUILD_DIR + '..\\nvme_B0_image_raid\\'

TMP_DIR_LIST = [BUILD_DIR + '_out_2T_3D_0', BUILD_DIR + '_out_2T_3D_1',
                BUILD_DIR + '_out_2T_2D_0', BUILD_DIR + '_out_2T_2D_1',
                BUILD_DIR + "_feedback"]

FW_PAC_DIR = BUILD_DIR +'Image_creator\\Artemis_dual_core_firmware_package\\'

TMP_IMAGE_FILE_LIST = [FW_PAC_DIR + "image_firmware.bin", FW_PAC_DIR + "misc_cfg.bin"]


TMP_SEC_FILE_LIST = ["image_firmware.bin", "C0_ATCM_0", "C0_BTCM", "C0_SDATA",
                     "C0_UNSAFE_CODE_DATA", "C1_ATCM", "C1_BTCM", "C1_INIT_CODE_BASE",
                     "C1_PS_CODE", "C1_UNSAFE_CODE_DATA", "INIT_CODE_BASE",
                     "SDATA", "SLOW_DATA", "Artemis2_ASIC_NVME_FTL.lst",
                     "Artemis2_ASIC_NVME_FTL_0.axf", "Artemis2_ASIC_NVME_FTL_1.axf"]


#clean all the build output
def start() :
    try :
        shutil.rmtree(IMAGE_DIR)
    except Exception:
        pass

    try:
        shutil.rmtree(IMAGE_RAID_DIR)
    except Exception:
        pass
    
    for each_dir in TMP_DIR_LIST:
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
    return

if __name__ == "__main__":
    start()       
