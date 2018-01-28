#!/usr/bin/evn python
#coding:utf-8

import sys

fileName = "startLunBgrTask_flow.xml"

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

try:
  tree = ET.parse(fileName)     #打开xml文档
  #root = ET.fromstring(country_string) #从字符串传递xml
  root = tree.getroot()         #获得root节点
except Exception :
  print("Error:cannot parse file:" + fileName)
  sys.exit(1)

#print("root : " + root.tag + "  " + str( root.attrib))

#func_name = root.attrib["name"]

#属性统一转换为小写字符串比较
#root_path = root.find("root").text
#is_raid = (root.find("raid").text.lower() == "true")

# print("func name is [%s]." %func_name)
# print ("need in work ctrl : %d" %needInWorkCtrl)
# print("sync: %d" %isSync)


def getAllItemList():
    allElement = list(root)
    return allElement


def iter_pro():
    allElement = list(root)
    count = 0

    for element in allElement:
      if ("project" == element.tag.lower()):
        #print("%s name is %s, type is %s." %(element.tag, element.get("name"), element.find("root")))
        project_name = element.get("name")
        root_path = element.find("root").text
        raid = (element.find("raid").text.lower() == 'true')
        burner = (element.find("burner").text.lower() == 'true')
        #print("project name %s, path %s, support raid %s, need burner %s."%(project_name, root_path, raid, burner))
        count+=1
        yield (project_name, root_path, raid, burner)
    return count

if __name__ == '__main__':
    print("list all")
    for name, path, raid, burner in iter_pro():
        print("project name %s, path %s, support raid %s, need burner %s."%(name, path, raid, burner))
    exit()

    allElement = list(root)
    print ("="*20)
#    print("The project: %s root is %s, support raid %s." % (func_name, root_path, is_raid))
    for element in allElement:
      if ("project" == element.tag.lower()):
        print("%s name is %s, type is %s." %(element.tag, element.get("name"), element.find("root").text.lower()))

      if ("flow" == element.tag.lower()):
        print("%s name is %s." %(element.tag, element.get("name")))
    print("="*20)
#for action in root.iterfind("action"):
#  actionName = action.get("name")
#  print("%s name is %s" %(action.tag, actionName))
#  print(list(action))
  #name = country.get('name')

#print root[0][1].text   #通过下标访问
#print(root[2].tag)
#print root[2].attrib

#lst_node = root.getiterator("action")
#for node in lst_node:
#  print(node)


