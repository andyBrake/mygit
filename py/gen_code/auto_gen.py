#!/usr/bin/evn python
#coding:utf-8

import commands
import parse_xml
import gen_util

WRITE_TO_FILE = False

# (status, output) = commands.getstatusoutput('pwd')
(status, output) = commands.getstatusoutput('rm -f ./output/*')
print status, output


allElement = parse_xml.getAllItemList()
for element in allElement:
  if ("action" == element.tag.lower()):
    isAsync = element.find("type").text.lower()
    name = element.get("name")
    # print("%s name is %s, type is %s." %(element.tag, name, isAsync))
    actionEle = gen_util.Action(element.find("type").text.lower(), element.get("name"))
    #print(actionEle)
    code_text = actionEle.gen_code(WRITE_TO_FILE)
    #code_text = actionEle.gen_func_code(WRITE_TO_FILE)
    print(code_text)

  if ("flow" == element.tag.lower()):
    print("%s name is %s." %(element.tag, element.get("name")))
