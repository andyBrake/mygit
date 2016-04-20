#coding=utf-8
import urllib
import re

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "%.2f%%"% percent

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    x = 0
    for imgurl in imglist:
        print ('start to download ' +str(x)+'.jpg') 
        urllib.urlretrieve(imgurl,'%s.jpg' % x, callbackfunc)
        x+=1
    return imglist

html = getHtml("http://www.meizitu.com/a/5196.html")
img = getImg(html)

#for imgurl in img
#print img
print "download over!"
