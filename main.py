#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file:
date: 4/4/14
Descrition:
    This file test the gtk gui capabilities.

Author: Caio Rodrigues
"""

#-------------------------------------------------#
# ============== IMPORTS =========================#
#
import pygtk
pygtk.require('2.0')
import gtk



#--------------------------------------------------#
# ============ GLOBAL VARIABLES ===================#
#

from encfs import Encfs


class Base:
    """
    Main window class
    """

    def __init__(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        #self.window.set_size_request(500, 500)
        self.window.set_title("Encfs Front End")
        self.window.connect("destroy", self.destroy)

        # Encrypted volumes
        self.volumes = []
        self.enc = Encfs()

        self.create_widgets()


    def create_widgets(self):


        self.label1 = gtk.Label("Encrypted Volume Path")
        self.label2 = gtk.Label("Mount Point Path")

        # Encryption path text box
        #
        self.entry_enc = gtk.Entry()
        self.entry_enc.set_tooltip_text("Path to encrypted volume")


        # Mount point path text box
        #
        self.entry_mnt = gtk.Entry()
        self.entry_mnt.set_tooltip_text("Path to mount point")



        # Password Entry
        self.entry_pass = gtk.Entry()
        self.entry_pass.set_tooltip_text("Path to mount point")


        # Mount button
        self.button_mount = gtk.Button("Mount")
        self.button_mount.set_tooltip_text("Mount encrypted volume")
        self.button_mount.connect("clicked", self.open_encrypted)

        # Unumount button
        self.button_umount = gtk.Button("Mount")
        self.button_umount.set_tooltip_text("Mount encrypted volume")
        self.button_umount.connect("clicked", self.close_encrypted)


        # Button1
        # Declare widget
        self.button1 = gtk.Button("EXIT")
        self.button1.set_tooltip_text("Close the main window")
        self.button1.connect("clicked", self.destroy)



        #self.filechooser = gtk.FileChooserDialog\
        #    ("Open ...", None, gtk.FILE_CHOOSER_ACTION_OPEN,
        #     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,  gtk.RESPONSE_OK))


        # Create container to button
        fixed = gtk.Fixed()
        fixed.put(self.button1, 0, 200)
        fixed.put(self.entry_enc, 100, 30)
        fixed.put(self.entry_mnt, 100, 50)
        fixed.put(self.entry_pass, 100, 70)
        fixed.put(self.button_mount, 0, 0)
        fixed.put(self.button_umount,0 ,30)

#        fixed.put(self.filechooser, 50, 30)

        self.window.add(fixed) # Add fixed container to main window
        # Show main window
        self.window.show_all()

    def main(self):
        gtk.main()

    def destroy(self, widget, data=None):
        """
        Kill the app when the app is closed
        """
        print "App closed"
        gtk.main_quit()

    def open_encrypted(self, widget, data=None):
        print "Mounting encrypted volume"
        print "Encrypted", self.entry_enc.get_text()
        print "Mounted", self.entry_mnt.get_text()

        encp = self.entry_enc.get_text()
        mntp = self.entry_mnt.get_text()
        password = self.entry_pass.get_text()

        self.enc = Encfs()
        self.enc.open(encp, mntp, password)


    def close_encrypted(self, widget, data=None):
        print "Closing encrypted volume"
        print "Encrypted", self.entry_enc.get_text()
        print "Mounted", self.entry_mnt.get_text()

        self.enc.close()



if __name__ == "__main__":
    base = Base()
    base.main()