#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


encfs ", "-o", "allow_other",

"""

import os
import logging
import logging.config

LOG_ENABLE = False

LOG_SETTINGS = {
    # --------- GENERAL OPTIONS ---------#
    'version': 1,
    'disable_existing_loggers': False,

    # ---------- LOGGERS ---------------#
    'root': {
        'level': 'NOTSET',
        'handlers': ['console'], #['filecsv', 'file', 'console'],
        'enable'  : True,
        'propagate' : False
    },

    # ---------- HANDLERS ---------------#
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
        'rotatingfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'NOTSET',
            'formatter': 'detailed',
            'filename': __file__.split('.')[0] + "_rot.log",
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'NOTSET',
            'formatter': 'detailed',
            'filename': __file__.split('.')[0] + ".log",
            'mode': 'w',
        },
        'filecsv': {
            'class': 'logging.FileHandler',
            'level': 'NOTSET',
            'formatter': 'csv1',
            'filename': __file__.split('.')[0] + ".csv",
            'mode': 'w',
        },
        'tcp': {
            'class': 'logging.handlers.SocketHandler',
            'level': 'NOTSET',
            'host': '127.0.0.1',
            'port': 9020,
            'formatter': 'detailed',
        },
    },

    # ----- FORMATTERS -----------------#
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(funcName)s() ' \
                      '%(levelname)-8s %(message)s',
        },
        'csv1': {
            'format': '%(asctime)s,%(module)-4s,line:%(lineno)-4d,%(funcName)s(),' \
                      '%(levelname)-4s,%(message)s',
        },
        'email': {
            'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
                      'Line: %(lineno)d\nMessage: %(message)s',
        },
    },
}



if LOG_ENABLE:
    logging.config.dictConfig(LOG_SETTINGS)
    log = logging.getLogger("root")
else:
    log = logging.getLogger()



log.info("==== starting logging =====")


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

    log.info({"encdir": encdir, "plaindir": plaindir, "password": password})

    if not os.path.isdir(encdir):
        mkdir(encdir)

    if not os.path.isdir(plaindir):
        mkdir(plaindir)

    from subprocess import call, PIPE, STDOUT
    import sys


    cmd = " ".join(["encfs", "--standard" ,'--extpass="%s"' % password ,encdir, plaindir])

    log.info("cmd %s" % cmd)

    r = call(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    log.info("r = %s" % r)

    if r != 0:
        return "Error -- encfs volume already exists"


def open_encfs(encdir, plaindir, password, keyfile=""):
    from subprocess import  PIPE,Popen

    mkdir(encdir)
    mkdir(plaindir)

    #  "-o", "allow_other"

    #print cmd
    env = os.environ.copy()
    if keyfile:
        env['ENCFS6_CONFIG'] = keyfile

    cmd = ["/usr/bin/encfs", "-o", "nonempty", "--standard", "-S", encdir, plaindir]
    # Returns 1 - If not sucessful and 0 if sucessful
    try:
        p = Popen(cmd,  stdout=PIPE, stdin=PIPE, stderr=PIPE, env=env)
        out = p.communicate(password)
    except Exception as err:
        print str(err)
        return False

    return p.returncode == 0

class Encfs():
    """
    Wrapper class to encfs encryption tool.


    """

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
        log.info("start Encfs.open()")

        log.debug(dict(zip(["encdir", "plaindir", "password", "keyfile", "mount"],
                              [encdir, plaindir, password, keyfile, mount] )))

        import os

        self.encdir   = encdir
        self.plaindir = plaindir
        self.password = password
        self.keyfile =  keyfile

        if mount:
            #create_encfs(encdir, plaindir, password)
            status = open_encfs(encdir, plaindir, password, keyfile)
            log.debug("status = %s" % status)

            if keyfile == "":
                keyfile = os.path.join(encdir, default_keyfile)

                log.debug("keyfile = %s" % keyfile)

                self.keyfile = keyfile

            fp = open(keyfile)
            self.keydata = fp.read()
            log.debug("self.keydata : %s" % self.keydata)

            fp.close()

            return status

        return None

    def mount(self, plaindir="", password ="", keyfile=""):

        log.info("Mounting directory")
        log.debug({"plaindir": plaindir, "password": password, "keyfile": keyfile})

        if plaindir == "":
            plaindir = self.plaindir

        if password == "":
            _password = self.password
        else:
            _password = password

        return self.open(self.encdir, plaindir, _password, keyfile)

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

        #from subprocess import call
        from subprocess import Popen, PIPE
        #call(["fusermount", "-uz" ,self.plaindir])
        from subprocess import Popen, PIPE

        log.info("Closing encrypted volume")

        p = Popen(["fusermount", "-uz" ,self.plaindir], stderr=PIPE, stdout=PIPE, stdin=PIPE)
        out, err = p.communicate()
        log.debug({"out": out, "err": err})

    def __show__(self):
        txt  = "\nencdir\t" + self.encdir
        txt += "\nplaindir\t" + self.plaindir
        #txt += "\npassword\t" + self.password
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
