#-*-coding:utf-8-*-

import os
import subprocess
#Firstly, you must create a file named 'svnlog.txt' in c: root dir
#after run this script, you will find a dir temp_ver_XX, this is checkout tag, use it to build

#svn tool installed path
SVN_CMD = r'"C:\Program Files (x86)\Subversion\bin\svn"'

#where you want to checkout tag branch
PRO_ROOT = r'C:\Users\huangfa\workspace\trunk_code'

def create_tag(number, tag_name, comment = "release create tag"):
    base_svn_url = 'svn://10.68.79.211/ArtemisPlus/Firmware/trunk'
    tag_svn_url = 'svn://10.68.79.211/ArtemisPlus/Validation/FW/tags/4.5.0.' + str(tag_name)
    tag_dir_prex = '\\temp_ver_'

    if number != 0 :
        ver_para = ' -r ' +  str(number) + ' '
    else :
        ver_para = ' '
    cmd = SVN_CMD +' copy ' + base_svn_url + ver_para + tag_svn_url + ' -F c:\svnlog.txt ' # + ' -m ' + comment
    print(cmd)
    subprocess.call(cmd, shell=True)

    #update local code, to checkout new tag code
    os.chdir(PRO_ROOT)
    cmd = SVN_CMD + ' checkout ' + tag_svn_url + ' .' + tag_dir_prex +str(tag_name)
    print(cmd)
    subprocess.call(cmd, shell=False)

    tag_path = PRO_ROOT + tag_dir_prex+str(tag_name)
    print(tag_path)

    return tag_path

def edit_version(version_num, tag_path):
    version_file = tag_path + r'\version.h'
    config_file =  tag_path + r'\build\Image_creator\Artemis_dual_core_firmware_package\config_combimage.txt'
    #edit the version.h
    data = ''
    with open(version_file, 'r+') as f:
        for line in f.readlines():
            if(line.find('#define NVME_FW_VER_BUILD ') == 0):
                line = '#define NVME_FW_VER_BUILD   %d' % (version_num) + '\n'
                print("edit ver %d, %s\n"%(version_num, version_file))
                print(line)
            data += line

    with open(version_file, 'r+') as f:
        f.writelines(data)
    print("finish edit version.h")

    #edit the config_combimage.txt
    data = ''
    with open(config_file, 'r+') as f:
        for line in f.readlines():
            if(line.find('VERSION = 4.5.0.') == 0):
                line = 'VERSION = 4.5.0.%d' % (version_num) + '\n'
                print("edit ver %d, %s\n"%(version_num, version_file))
                print(line)
            data += line

    with open(config_file, 'r+') as f:
        f.writelines(data)
    print("finish edit config_combimage.txt")
    return

if __name__ == '__main__':
    src_ver_num = 0 #which version you want create tag, if 0 will use the latest version
    tag_name = 98 #the new tag name, will add a pre 4.5.0, so the full tag name is 4.5.0.98

    os.chdir(PRO_ROOT)
    tag_path = create_tag(src_ver_num, tag_name)
    edit_version(tag_name, tag_path)
    print("\nFinish\n")