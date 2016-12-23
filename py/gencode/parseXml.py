#!/usr/bin/evn python
#coding:utf-8

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
import sys

try:
  tree = ET.parse("country_data.xml")     #打开xml文档
  #root = ET.fromstring(country_string) #从字符串传递xml
  root = tree.getroot()         #获得root节点
except Exception, e:
  print "Error:cannot parse file:country.xml."
  sys.exit(1)

print("root : " + root.tag + "  " + str( root.attrib))

for child in root:
  print child.tag, "---", child.attrib

print "*"*10
print root[0][1].text   #通过下标访问
print(root[1].tag)
#print root[0].tag, root[0].text
print "*"*10

for neighbor in root.iter('rank'):
  print neighbor.attrib

for country in root.findall('country'): #找到root节点下的所有country节点
  rank = country.find('rank').text   #子节点下节点rank的值
  name = country.get('name')      #子节点下属性name的值
  print name, rank

#修改xml文件
for country in root.findall('country'):
  rank = int(country.find('rank').text)
  if rank > 50:
    root.remove(country)

tree.write('output.xml')