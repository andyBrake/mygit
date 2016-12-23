#!/usr/bin/evn python
#coding:utf-8



from string import Template



def gen_func(rt='char'):
    func_text = '''
$ret_type_head $func_name
{
    return${ret_type_tail};
}'''
    
    func = Template(func_text)
    if rt == "void":
        ret_tail = ''
    else :
        ret_tail = " " + rt
        
    return func.substitute(ret_type_head = rt, ret_type_tail = ret_tail, func_name = 'test_func');

template = ""

print("hello")

with open("startTask_template") as template_file:
    template = template_file.read()

startTask = Template(template)

ret_file = startTask.substitute(task_func="startLunTask", inWorkCtrl="TRUE")

print (ret_file)