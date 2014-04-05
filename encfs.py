#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

#-------------------------------------------------#
# ============== IMPORTS =========================#
#

#--------------------------------------------------#
# ============ GLOBAL VARIABLES ===================#
#


default_keyfile =".encfs6.xml"

def mkdir(path):
    """"
    Create directory if not exists
    equivalent to mkdir -p path

    """
    import os

    if os.path.isdir(path) == False:
        os.makedirs(path)


def create_encfs(encdir, plaindir, password=""):
    import os

    encdir = os.path.expanduser(encdir)
    plaindir = os.path.expanduser(plaindir)

    if not os.path.isdir(encdir):
        mkdir(encdir)

    if not os.path.isdir(plaindir):
        mkdir(plaindir)

    from subprocess import call, PIPE, STDOUT
    import sys


    cmd = " ".join(["encfs", "--standard" ,'--extpass="%s"' % password ,encdir, plaindir])
    r = call(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    if r != 0:
        return "Error -- encfs volume already exists"


def open_encfs(encdir, plaindir, password, keyfile=""):
    from subprocess import call, PIPE, STDOUT
    import sys

    print "keyfile =", keyfile

    mkdir(encdir)
    mkdir(plaindir)

    if keyfile !="":

        keyfile = "ENCFS6_CONFIG=%s" % keyfile

    cmd = " ".join([keyfile, "encfs", "--standard" ,'--extpass="echo %s"' % password ,encdir, plaindir])

    print cmd

    r = call(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return r


class Encfs():

    def __init__(self):
        self.encdir   = ""
        self.plaindir = ""
        self.password = ""
        self.keyfile = ""


    def open(self, encdir, plaindir="", password="", keyfile="", mount=True):
        """
        Open or create encrypted volume if it don't exist.

        encdir -- Encrypted directory
        plaindir -- Plain directory
        """

        import os

        self.encdir   = encdir
        self.plaindir = plaindir
        self.password = password
        self.keyfile =  keyfile

        if mount:
            #create_encfs(encdir, plaindir, password)
            open_encfs(encdir, plaindir, password, keyfile)

            if keyfile == "":
                keyfile = os.path.join(encdir, default_keyfile)
                self.keyfile = keyfile

            fp = open(keyfile)
            self.keydata = fp.read()
            fp.close()

    def mount(self, plaindir="", password ="", keyfile=""):

        if plaindir == "":
            plaindir = self.plaindir

        if password == "":
            _password = self.password
        else:
            _password = password

        self.open(self.encdir, plaindir, _password, keyfile)


    def create(self, password, encdir="", keyfile=""):
        """
        Create encrypted directory only, however
        don't open it.

        If encdir == ""  creates only the keyfile
        if both empty creates the keyfile in the memory

        """
        import tempfile
        import os

        plaindir = tempfile.mkdtemp()
        self.plaindir = plaindir



        if keyfile == '':
            p = tempfile.NamedTemporaryFile() #"/tmp/dh8712aahj"
            _keyfile = p.name
        else:
            _keyfile = keyfile

        if encdir == '':
            _encdir = tempfile.mkdtemp()
        else:
            _encdir  = encdir
            if keyfile == "":
                _keyfile = ""

        open_encfs(_encdir, plaindir, password, keyfile=_keyfile)


        if _keyfile != "":
            fp = open(_keyfile)
            self.keydata = fp.read()
            fp.close()
        else:
            self.keyfile = os.path.join(encdir, default_keyfile)
            fp = open(self.keyfile)
            self.keydata = fp.read()
            fp.close()

        print _encdir
        print plaindir
        print _keyfile

        self.close()

        if keyfile == "":
            p.close()

        #self.plaindir = ""



    def newkey(self, password):

        keyfile = "/tmp/"

    def goto_plain(self):
        import os
        os.chdir(self.plaindir)

    def close(self, mnt=""):
        """
        Unmount encrypted directory
        """


        from subprocess import Popen, PIPE, STDOUT
        proc = Popen(["fusermount", "-uz" ,self.plaindir])

    def __show__(self):
        txt  = "\nencdir\t" + self.encdir
        txt += "\nplaindir\t" + self.plaindir
        txt += "\npassword\t" + self.password
        txt += "\nkeyfile\t" + self.keyfile

        return txt

    def __repr__(self):
        return self.__show__()

    def __str__(self):
        return self.__show__()


import time

#enc = Encfs()

#enc.open(encdir="/home/tux/tmp/e1",
#         plaindir="/home/tux/tmp/p1",
#         password="tux",
#         keyfile="/home/tux/tmp/key.encfs6.xml" )


#enc.open("/home/tux/encrypted", "/home/tux/mnt", password="tux", mount=False)
#enc.mount("/home/tux/mnt")
#enc.create(password="tux", encdir="/home/tux/encrypted")

#print enc
#print enc.keydata
#import IPython ;  IPython.embed()

#enc.mount('/home/tux/mnt')

#enc.close()