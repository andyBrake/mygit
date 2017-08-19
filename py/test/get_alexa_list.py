import csv
from zipfile import ZipFile
from StringIO import StringIO
from downloader import Downloader

alexa_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
zipfile = './urllist.zip'

#D = Downloader()
#zipped_data = D(alexa_url)

zipped_data = zipfile
if None == zipped_data:
    print 'download failed!'
    exit(1)

urls = []

with open('urllist.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

for eachUrl in rows:
    urls.append('http://' + eachUrl[1])
    print eachUrl[1]

print 'finish'
print urls