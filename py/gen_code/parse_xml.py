#!/usr/bin/evn python
#coding:utf-8

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
import sys

fileName = "startLunBgrTask_flow.xml"

try:
  tree = ET.parse(fileName)     #打开xml文档
  #root = ET.fromstring(country_string) #从字符串传递xml
  root = tree.getroot()         #获得root节点
except Exception, e:
  print ("Error:cannot parse file:" + fileName)
  sys.exit(1)

#print("root : " + root.tag + "  " + str( root.attrib))

func_name = root.attrib["name"]

#属性统一转换为小写字符串比较
isSync = (root.find("type").text.lower() == "sync")
needInWorkCtrl = (root.find("inWorkCtrl").text.lower() == "true")

# print("func name is [%s]." %func_name)
# print ("need in work ctrl : %d" %needInWorkCtrl)
# print("sync: %d" %isSync)
if __name__ == '__main__':
    allElement = list(root)
    print ("="*20)
    print("The flow %s sync type is %s, needInWortCtrl %s" % (func_name, isSync, needInWorkCtrl))
    for element in allElement:
      if ("action" == element.tag.lower()):
        print("%s name is %s, type is %s." %(element.tag, element.get("name"), element.find("type").text.lower()))

      if ("flow" == element.tag.lower()):
        print("%s name is %s." %(element.tag, element.get("name")))
    print("="*20)

def getAllItemList():
    allElement = list(root)
    return allElement

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


