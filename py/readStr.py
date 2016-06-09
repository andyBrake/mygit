#!/bin/bash/python3.5

from io import StringIO
f=StringIO('dfdfdf\n')
while True:
    s = f.readline()
    if s == '':
        break
    print(s.strip())

