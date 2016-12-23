#!/usr/bin/evn python
#coding:utf-8

from string import Template

#
# def gen_func(rt='char'):
#     func_text = '''
# $ret_type_head $func_name
# {
#     return${ret_type_tail};
# }'''
#     func = Template(func_text)
#     if rt == "void":
#         ret_tail = ''
#     else :
#         ret_tail = " " + rt
#     return func.substitute(ret_type_head = rt, ret_type_tail = ret_tail, func_name = 'test_func');

# template = ""

#main test code:
if __name__ == '__main__':
    with open("startTask_template") as template_file:
        template = template_file.read()

    startTask = Template(template)

    ret_file = startTask.substitute(task_func="startLunTask", inWorkCtrl="TRUE", FLOW_NAME="START_LUN_TASK")

    print (ret_file)

#Flow and Action super class
class Step:
    def __init__(self, syncType, name):
        self.type = ""  #用于flow和action区别
        self.name = name
        self.syncType = syncType
        self.moudleName = "LUN"
        self.enum_name = self.__get_enum_name()
        self.func_name = self.__get_func_name()

    def __str__(self):
        print("-------------------------------------")
        print("name           :  %s" % self.name)
        print("type           :  %s" % self.syncType)
        print("moudle         :  %s" % self.moudleName)
        print("enum name      :  %s" % self.enum_name)
        print("main func name :  %s" % self.func_name)
        return "-------------------------------------"

    #生成函数的name
    def __get_func_name(self):
        func_name = self.name + "Func"
        return func_name

    #判断该step是否已经存在了
    def isExist(self):
        return False

    #新增枚举定义
    def __get_enum_name(self):
        enumName = self.moudleName + "_" + self.name
        return enumName

    #将代码 写入文件
    def __writeToFile(self, fileName, code_text):
        wholeName = "./output/" + fileName
        with open(wholeName, 'w') as file:
            file.write(code_text)
            file.write("\n\n")

    #生成主函数代码
    def gen_func_code(self, writeToFile = False):
        with open("action_template") as func_file:
            func_text = func_file.read()
            func = Template(func_text)

        if self.syncType == 'async':
            ret_tail = "RETURN_ASYNC"
        else :
            ret_tail = "RETURN_SYNC"

        code_text = func.substitute(isAsync = ret_tail,
                                    action_name = self.func_name,
                                    func_name = self.name + self.type + 'Func');
        if writeToFile:
            self.__writeToFile("aaa", code_text)

        return code_text

    #生成枚举定义代码
    def gen_enum_code(self, writeToFile = False):
        with open("enum_define_template") as func_file:
            func_text = func_file.read()
            enumCode = Template(func_text)

        code_text = "enum_code  \n"
        #code_text = func.substitute(isAsync = ret_tail, action_name = func_name, func_name = self._name + 'ActionFunc');
        if writeToFile:
            pass

        return code_text

    #生成策略驱动表代码
    def gen_strage_code(self, writeToFile = False):
        return "[strgae]\n"


    #生成总的代码
    def gen_code(self, writeToFile = False):

        if self.isExist():
            print("[%s] is already exist." % (self.name))
        else:
            retCode = ''
            #生成enum的定义代码
            retCode += self.gen_enum_code()

            #生成strage驱动表代码
            retCode += self.gen_strage_code()

            #生成task处理函数代码
            retCode += self.gen_func_code()

            return retCode

#Action class 继承 Step class
class Action(Step):
    def __init__(self, syncType, name):
        Step.__init__(self, syncType, name)
        self.type = "Action"

class Flow(Step):
    def __init__(self, syncType, name):
        Step.__init__(self, syncType, name)
        self.type = "Flow"

