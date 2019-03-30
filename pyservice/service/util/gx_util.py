# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:01:38 2018

@author: Lidh
"""
import json
import sys
from urllib import parse
from urllib import request
def getData():
    f=request.urlopen(sys.argv[1])
    strs=f.read()
    return json.loads(strs.decode('utf-8'))
def saveData(data):
    datao=parse.urlencode(data).encode('utf-8')
    request0=request.Request(sys.argv[2],datao)
    res=request.urlopen(request0).read().decode('utf-8')
    print(res)
    return res