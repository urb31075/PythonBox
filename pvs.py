#! /usr/bin/python
# -*- coding: utf-8 -*-

# Клонирует проект из GitLab, рекурсивно вставляет в начало файла заголовок для
# бесплатной версии PVS-Studio, перекомпилирует проект и запускает PVS-Studio

import os
import sys
import fnmatch
import re
import shutil

#Функция ищет все файлы с именем filename во всех подкаталогах каталога catalog
def find_files(root, regex):
    find_files = []
    pattern = re.compile(regex)
    for folder, subdirs, files in os.walk(root):
       for filename in files:
          if pattern.match(filename):
             fullname = os.path.join(folder, filename)
             fullname_abs = os.path.abspath(fullname)
             find_files +=[fullname_abs]
    return find_files

print("PVSAddon start!")

workdir = os.path.abspath(os.curdir) + "/TMPDATA"
os.system("sudo rm -r -f " +  workdir)
os.mkdir(workdir)
os.chdir(workdir)
os.system("git --version")
os.system("git clone git@gitlab.baum-inform.ru:baum-inform/swarm.git")

regex1 = fnmatch.translate('*.cpp')
regex2 = fnmatch.translate('*.c')
regex3 = fnmatch.translate('*.hpp')
regex4 = fnmatch.translate('*.h')
regex = '(' + regex1 + '|' + regex2 + '|' + regex3 + '|' + regex4 + ')'
print (regex)

root = workdir + "/swarm"
if len (sys.argv) > 1:
   root = sys.argv[1]

print ('root=' + root)

for file in find_files(root, regex):
    print(file)
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    f = open(file, "w")
    f.write("// This is an open source non-commercial project. Dear PVS-Studio, please check it. \n");
    f.write("// PVS-Studio Static Code Analyzer for C, C++, C#, and Java: http://www.viva64.com \n");
    f.writelines(lines)
    f.close()

print("Build!")
os.chdir(workdir+"/swarm")
os.system("git submodule init")
os.system("git submodule update")
os.system("meson build")
os.system("/usr/bin/ninja -C build")
os.chdir(workdir+"/swarm/build")
os.system("pvs-studio-analyzer analyze -o PVS-Studio.log")
os.system("plog-converter -t html PVS-Studio.log -o PVS-Studio.html")
os.system("cp " + workdir + "/swarm/build/PVS-Studio.html /home/urb")
print("PVSAddon finish!")
