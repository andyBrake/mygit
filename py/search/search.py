#!/usr/bin/evn python
#coding:utf-8

import os
import re

file_list = os.listdir(".")
pattern = re.compile(r'VOLUME_FATAL')

for each_file in file_list:
    if os.path.isfile(each_file):
        a,b = os.path.splitext(each_file)
        if b == "":
            print("to search %s"%a)
            with open(a) as text:
                context = text.read()
               # context = '''123VOLUME_FATALabc\n'''
                match = pattern.search(context)
                if match:
                    print("find in file : %s : " % (a))
                    #print(match)
                    #print(match.lastindex)
                    #print(match.pos)
                else:
                    print("not find")
               #     print(match.string)
               # print(context)
        

