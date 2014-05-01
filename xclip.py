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

class Xclip:
    """
    Python wrapper to  xclip utility.
    """

    def __init__(self):
        self.content = []

    def __repr__(self):
        return self.read()

    def __str__(self):
        return self.read()

    def read(self):
        """
        Get clipboard content
        """

        from subprocess import Popen, PIPE

        p = Popen("xclip -o -selection cliboard ", shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        output = p.stdout.read()
        self.content.append(output)
        return output

    def readf(self, mode="rb"):
        """
        Read file from clipboard and return content.

        Returns ( filename, data)
        """
        # Filepath from clipboard

        fname = self.read()

        try:
            fp = open(fname, mode)
            data = fp.read()
            fp.close()

        except:
            return fname

        return data


    def write(self, string):
        from subprocess import Popen, PIPE

        p = Popen("xclip -i -selection cliboard", shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        #o = p.communicate(string)
        p.stdin.write(string)
        p.stdin.close()
        #return o



#c = Xclip()
#print c.write("xxxxxxxxxx Hello worldsdasdasd clipboard xxyadasfasf123456")

#print c.read()

#print c.readf()[0]