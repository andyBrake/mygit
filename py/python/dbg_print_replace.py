import os
import re
import shutil

TAR = '''Debug_Log(cLogCore, cLogDebug, ("'''

SUB_STR = '''Debug_log'''

def find_match_print(data) :
    p = r'dbg_printf_always'
    pattern = r'[\s\t]{1}dbg_printf_always\s*\("{1}[\w\s:%\.,\n><]+'
    pattern1 = r'[\s\t]+dbg_printf_always\s*\("{1}[\w\s:%\.,\n><]+"{1}[,\w\.\s\n->]*?\);[^"\(\w]'
    pattern2 = r'dbg_printf_always\s*\("{1}[\w\s:%\.,\n><]+"{1}[,\w\.\s\n->]*?\);' #[,\w\.\s\n->]*?\);[^"\(\w]

    testP1 = r'dbg_printf_always\('
    subP1  = '''Debug_Log(cLogSys, cLogInfo, ('''


    ret = re.findall(testP1, data, re.S|re.M)
    print("find %d result."%len(ret))

    result, number = re.subn(testP1, subP1, data, re.S|re.M)
    print("sub %d print."%number)

    with open(NEW_FILE, "w+") as new_file:
        new_file.write(result)

    #for x in ret:
    #    print(x)

    return ret
    #if match:
     #   print( match.group())

def replace_step1(line_data, new_file):
    #testP1 = r'\s{1}dbg_printf_always\('   #this pattern is for dbg_printf_always
    #testP1 = r'\s{1}dbg_printf_nts\('    #this pattern is for dbg_printf_nts
    testP1 = r'\s{1}dbg_printf_err\('   #this pattern is for dbg_printf_err
    subP1 = ''' DebugE_Log(cLogSys, cLogError, ('''
    ret = 0

    result, number = re.subn(testP1, subP1, line_data)
    if number != 0 :
        new_file.write(result)
        ret = 1
        #print("replace one line. [%s]"%line_data)
    else :
        new_file.write(line_data)
        #print("err in [%s]"%line_data)
        ret = 0
    return ret

#after replace all the Debug_Log, must add ) behind );
def replace_step2(step1_file, step2_file):
    p = r'DebugE_Log\(.*?;'
    ret = 0

    with open(step1_file, 'r') as file:
        data = file.read()
        ret = re.findall(p, data, re.S | re.M)
        print("step 2 find %d to replace." % len(ret))

        for each in ret:
            if each[-2] == ')' and each[-3] == ')':
                pass
            data = data.replace(each, each[:-1] + ");")

        with open(step2_file, "w+") as out_file:
            out_file.write(data)
    return ret

def process_single_file(input_file):
    print("to process the file %s"%input_file)

    STEP1_FILE = input_file[:-2] + "_step1" + ".c"
    STEP2_FILE = input_file[:-2] + "_step2" + ".c"

    #step 1
    cnt = 0
    new_file = open(STEP1_FILE, 'w+')
    with open(input_file, 'r') as file:
        all_line = []
        try :
            all_line = file.readlines()
        except Exception :
            print("%s is read error."%input_file)

        for each_line in all_line:
            cnt += replace_step1(each_line, new_file)
    new_file.close()

    if 0 == cnt:
        try:
            os.remove(STEP1_FILE)
        except Exception:
            print("PermissionError for %s"%STEP1_FILE)
        return
    print("step 1 replace %d count."%cnt)

    #step 2
    replace_step2(STEP1_FILE, STEP2_FILE)

    #step 3 copy the step2 file to cover source file
    # try :
    #     os.rename(input_file, input_file + ".bak")
    # except Exception:
    #     pass
    #
    # try :
    #     os.rename(STEP2_FILE, input_file)
    # except Exception:
    #     pass

    try :
        os.remove(STEP1_FILE)
    except Exception :
        pass
    try :
        os.remove(input_file)
    except Exception :
        pass

    os.rename(STEP2_FILE, input_file)
    #os.remove(STEP2_FILE)
    print("")

    return

def replace_in_dir(root):
    cur_pwd = os.getcwd()
    os.chdir(root)
    for root, dirs, files in os.walk(".\\", topdown=False):
        for name in files:
            if ".c" in name:
                process_file = os.path.join(root, name)
                #print(process_file)
                process_single_file(process_file)
        #for name in dirs:
        #    print(os.path.join(root, name))

    os.chdir(cur_pwd)
    return

def start():
    process_single_file("c:\\users\\huangfa\\workspace\\gitProject\\dualcore\\main.c")

    ROOT_BASE = "c:\\users\\huangfa\\workspace\\gitProject\\dualcore\\"
    DIR_LIST = ['utils\\', 'ukrnl\\', 'platform\\', 'boot\\']
    for each_dir in DIR_LIST:
        replace_in_dir(ROOT_BASE + each_dir)

if __name__ == '__main__':
    start()
    #out = process_single_file(IN_FILE)
    #print(out)

