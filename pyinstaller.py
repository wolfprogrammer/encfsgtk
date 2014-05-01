#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Installs python apps in user defined directory


"""

#-------------------------------------------------#
# ============== IMPORTS =========================#
#

import os
import sys

#--------------------------------------------------#
# ============ GLOBAL VARIABLES ===================#
#


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

def rm(file_):
    import os
    print "Removing ", file_
    os.system("rm -rf " + file_)




class DesktopEntry:

    def __init__(self):
        self.path = ""
        self.comment = ""
        self.icon = ""
        self.mimetype = ""
        self.categories = ['Application']
        self.encoding = "UTF-8"
        self.version  = "1.0"
        self.execute  = ""
        self.name     = "My application"
        self.type     = "Application"

        pass

    def create(self, filename, directory='~/Desktop'):

        import os
        directory = os.path.expanduser(directory)
        filename = os.path.join(directory, filename)


        categories = ";".join(self.categories)

        txt = "[Desktop Entry]"
        txt = "\n".join([txt,
                         'Type=%s'% self.type,
                         'Encoding=%s' % self.encoding,
                         'Name=%s'% self.name,
                         'Comment=%s' % self.comment,
                         'Exec=%s'% self.execute,
                         'Icon=%s'% self.icon,
                         'Categories=%s' % categories
                         ])

        fp = open(filename,'w')
        fp.write(txt)
        fp.close()

        print txt


class Installer:

    def __init__(self, bindir="~/bin", libdir="~/lib", icondir="~/.icons"):

        HOME = os.path.expanduser('~')

        self.binfiles  = [] # Files belonging to binary directory ( main or standalone)
        self.libfiles = [] # Files belonging to lib directory ( libraries )


        self.icon = False
        self.iconfile = ""

        self.home = HOME
        self.bindir = os.path.expanduser(bindir)
        self.libdir = os.path.expanduser(libdir)
        self.icondir = os.path.expanduser(icondir)
        self.desktop = os.path.expanduser("~/Desktop")

        self.execute = ""
        self.comment = ""
        self.name = ""


    def install(self):

        print "Installing ..."

        for f in self.binfiles:
            cp(f, self.bindir)

        for f in self.libfiles:
            cp(f, self.libdir)

        self.compile()

        if self.icon:
            self.shortcut_creator()

        print "---------------------"
        print "Installation done"
        print "---------------------"

    def shortcut_creator(self):

        # Create icon directory
        mkdir(self.icondir)
        # Move icon to icon directory
        cp(self.iconfile, self.icondir)

        d = DesktopEntry()
        d.comment = self.comment
        d.execute = self.execute
        d.name = self.name
        d.icon = os.path.join(self.icondir, self.iconfile)

        execute = self.execute
        if self.execute == "":
            execute = "python " + os.path.join(self.bindir, self.binfiles[0])

        d.execute = execute
        d.create(self.name + ".desktop")

    def uninstall(self):

        # Remove files from installation directory
        for f in self.binfiles:
            fpath = os.path.join(self.bindir, f)
            fpath2 = fpath.split('.')[0] + ".pyc"

            #print "rm  ",fpath
            rm(fpath)
            rm(fpath2)

        for f in self.libfiles:
            fpath = os.path.join(self.libdir, f)
            fpath2 = fpath.split('.')[0] + ".pyc"
            #print "rm ", fpath
            rm(fpath)
            rm(fpath2)

        print "---------------------"
        print "Uninstall done"
        print "---------------------"

    def pack(self):
        pass

    def compile(self):
        import compileall

        for f in self.binfiles:
            fpath = os.path.join(self.bindir, f)
            #print fpath
            compileall.compile_file(fpath)

        for f in self.libfiles:
            fpath = os.path.join(self.libdir, f)
            compileall.compile_file(fpath)


    def compile_bin(self):
        pass

    def createdoc(self):
        pass


def main():
    # import ipdb ; ipdb.set_trace() 
    pass


if __name__ == "__main__":
    main()