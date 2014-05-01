#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Install this project in user directory

Put the line in:
    export PYTHONPATH="$HOME/lib"

in ~/.profile

Conventions:

Binary directory:
    ~/bin
Libraries
    ~/lib

binfiles - will be copied to ~/bin
libfiles - will be copied to ~/lib

"""

from pyinstaller import Installer

p = Installer()

# ----------------------------------------------------#
#               INSTALLER SETTINGS                    #
#-----------------------------------------------------#
#
# Edit this section
#

p.icon = True
p.name = "Encfsgtk"
p.comment = "Encfs GUI Manager"

p.libfiles = [ 'encfs.py', 'pyinstaller.py']
p.binfiles  = [ 'encfsgtk.py']
p.iconfile = 'encfsgtk.png'


#=============== COMMAND LINE PARSER =======================#

import argparse
import sys

desc = " Python Interactive Installer "
parser = argparse.ArgumentParser(prog='mathpy', description=desc)

parser.add_argument("--install", action="store_true",  help="Run in interactive mode.")
parser.add_argument("--uninstall",action="store_true", help="<script> Run script.")
parser.add_argument("--compile-bin",action="store_true", help="Compile to binary object.")

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()

if args.install:
    p.install()
elif args.uninstall:
    p.uninstall()
elif args.compile_bin:
    p.compile_bin()


