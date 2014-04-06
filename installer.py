#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Install this project in user directory

Put the line in:
    export PYTHONPATH="$HOME/lib"

in ~/.profile

Convention: the file will be executed




"""

binfiles = [ 'encfsgtk.py',  'encfsgtk.png']
libfiles = [ 'encfs.py']
others   = [ 'icon.jpeg']
desktopfiles = ['encfsgtk.desktop']

libname  = 'encfs'

#-------------------------------------------------#
# ============== IMPORTS =========================#
#
import os
import sys

def get_resource_path(rel_path):
    """
    Return absolute path of file in the same
    directory as this file
    """
    import os
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource

def mkdir(path):
    """"
    Create directory if not exists
    equivalent to mkdir -p path

    """
    import os

    path = os.path.expanduser(path)

    if os.path.isdir(path) == False:
        os.makedirs(path)

def cp(src, dest):
    import os
    os.system("cp -v " + src + " " + dest)


HOME = os.path.expanduser('~')

# User binary directory
bindir = os.path.join(HOME, 'bin')

# User library directory
libdir = os.path.join(HOME, 'lib')

desktop = os.path.join(HOME, 'Desktop')

libpath = os.path.join(libdir, libname)

mkdir(bindir)
mkdir(libdir)
#mkdir(libpath)


for lib in libfiles:
    cp(lib, libdir)

for bin in binfiles:
    cp(bin, bindir)

for desk in desktopfiles:
    cp(desk, desktop)


print HOME