# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 09:56:28 2018

@author: Zcy
"""

import os, psutil

#set the base path of the freezed executable; (might change,
#check the last part for different architectures and python versions
basePath = r'D:\workspace\test\pyServiceALL\dist\pythonServiceAll'
appName = 'pythonServiceAll.exe'
#look for current processes and break when my program is found;
#be sure that the name is unique
for procId in psutil.pids():
    proc = psutil.Process(procId)
    if proc.name().lower() == 'pythonServiceAll.exe':
        break

deps = [p.path.lower() for p in proc.memory_maps() if p.path.lower().startswith(basePath)]
allFiles = []
for root, dirs, files in os.walk(basePath):
    for fileName in files:
        filePath = os.path.join(root, fileName).lower()
        allFiles.append(filePath)

#create a list of existing files not required, ignoring .pyc and .pyd files
unusedSet = set(allFiles) ^ set(deps)
unusedFiles = []
usedFiles=['api-ms-win','mkl_avx2','mkl_core','libiomp5md','mkl_def','mkl_intel_thread']
def canDelete(path0):
    for usedFile in usedFiles:
        if path0.find(usedFile)>-1:
            return False
    return True

for filePath in sorted(unusedSet):
    if filePath.endswith('dll') and canDelete(filePath):
        unusedFiles.append((filePath[len(basePath):], os.stat(filePath).st_size))

#print the list, sorted by size
for filePath, size in sorted(unusedFiles, key=lambda d: d[1]):
    print(filePath, size)
    try:
        os.remove(basePath+'\\'+filePath)
    except Exception as e:
        continue
