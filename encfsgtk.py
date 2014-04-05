#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file: encfsgtk.py
date: 4/4/14
Descrition:  This is a front-end to encfs.py encfs fuse file system.

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





class Base:
    """
    Main window class
    """

    def __init__(self):

        import os
        self.configfile = os.path.expanduser('~/.encfsgui.db')

        #self.configfile = "~/encfsgui.db"

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        #self.window.set_size_request(500, 500)
        self.window.set_title("Encfs Front End")
        self.window.connect("destroy", self.destroy)
        self.window.set_icon_from_file(get_resource_path("icon.jpeg"))

        # Encrypted volumes
        self.volumes = []
        self.enc = Encfs()

        self.create_widgets()
        self.pack_widgets()

        self.window.show_all()



    def create_widgets(self):
        """
        Define all gui widgets
        """
        import shelve
        import os
        self.label0 = gtk.Label("Volume name")
        self.label1 = gtk.Label("Encrypted Volume Path")
        self.label2 = gtk.Label("Mount Point Path")
        self.label3 = gtk.Label("Password")

        self.combo = gtk.combo_box_entry_new_text()
        self.combo.connect("changed", self.combo_text_changed)

        if os.path.isfile(self.configfile):


            data = shelve.open(self.configfile)
            volumes = data['volumes']
            entries = volumes.keys()
            #print entries
            #print data

            for e in entries:
                self.combo.append_text(e)


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
        self.entry_pass.set_tooltip_text("Encryption volume password")
        self.entry_pass.set_visibility(False)


        self.check1 = gtk.CheckButton(label="Open volume in file manager")
        self.check1.set_tooltip_text("Open volume in file manager after unencrypted")

        self.check_reverse = gtk.CheckButton(label="Reverse Encryption")
        self.check_reverse.set_tooltip_text("Encrypt a non empty directory\nThe encrypt data will be in the mount point")

        self.check_save = gtk.CheckButton(label="Save Password")


        # Mount button
        self.button_mount = gtk.Button("Open")
        self.button_mount.set_tooltip_text("Mount encrypted volume")
        self.button_mount.connect("clicked", self.open_encrypted)

        # Unumount button
        self.button_umount = gtk.Button("Close")
        self.button_umount.set_tooltip_text("Umount encrypted volume")
        self.button_umount.connect("clicked", self.close_encrypted)

        # Button save
        # Declare widget
        self.button_save = gtk.Button("Save")
        self.button_save.set_tooltip_text("Save all data")
        self.button_save.connect("clicked", self.save_data)

        # Button exit
        # Declare widget
        self.button_exit = gtk.Button("EXIT")
        self.button_exit.set_tooltip_text("Close the main window")
        self.button_exit.connect("clicked", self.destroy)

    def pack_widgets(self):
        """
        Define gui layout.
        """

        #vbox = gtk.VBox(spacing=10, homogeneous=True)
        vbox = gtk.VBox(spacing=10)

        self.label0.set_alignment(0, 0.5)
        self.label1.set_alignment(0, 0.5)
        self.label2.set_alignment(0, 0.5)
        self.label3.set_alignment(0, 0.5)

        hbox0 = gtk.HBox(spacing=10, homogeneous=True)
        hbox0.pack_start(self.label0, expand=True, fill=True)
        hbox0.pack_start(self.combo, expand=True, fill=True)


        hbox1 = gtk.HBox(spacing=10, homogeneous=True)
        hbox1.pack_start(self.label1, expand=True, fill=True)
        hbox1.pack_start(self.entry_enc, expand=True, fill=True)

        hbox2 = gtk.HBox(spacing=10, homogeneous=True)
        hbox2.pack_start(self.label2, expand=True, fill=True)
        hbox2.pack_start(self.entry_mnt, expand=True, fill=True)

        hbox3 = gtk.HBox(spacing=10, homogeneous=True)
        hbox3.pack_start(self.label3)
        hbox3.pack_start(self.entry_pass)

        vbox1 = gtk.VBox(spacing=10)
        vbox1.pack_start(self.check1)
        vbox1.pack_start(self.check_reverse)
        vbox1.pack_start(self.check_save)

        hbox4 = gtk.HBox(spacing=10, homogeneous=True)
        hbox4.pack_start(self.button_mount)
        hbox4.pack_start(self.button_umount)

        hbox5 = gtk.HBox(spacing=10, homogeneous=True)
        hbox5.pack_start(self.button_save)
        hbox5.pack_start(self.button_exit)


        vbox.pack_start(hbox0)
        vbox.pack_start(hbox1)
        vbox.pack_start(hbox2)
        vbox.pack_start(hbox3)
        vbox.pack_start(vbox1)
        vbox.pack_start(hbox4)
        vbox.pack_start(hbox5)

        self.window.add(vbox) # Add fixed container to main window
        # Show main window



    def main(self):
        gtk.main()

    #----------- GUI Signals -------------- #

    def destroy(self, widget, data=None):
        """
        Kill the app when the app is closed
        """
        #print "App closed"
        gtk.main_quit()

    def open_encrypted(self, widget, data=None):



        #print "Mounting encrypted volume"
        #print "Encrypted", self.entry_enc.get_text()
        #print "Mounted", self.entry_mnt.get_text()

        encp = self.entry_enc.get_text()
        mntp = self.entry_mnt.get_text()
        password = self.entry_pass.get_text()

        if password == "":
            return

        self.enc = Encfs()
        status = self.enc.open(encp, mntp, password)
        #print "--------opened -----------"

                #if self.check_reverse.get
        if self.check_reverse.get_active():
   
            #print "Opening in file manager"
            from subprocess import call, PIPE, STDOUT
            call(["xdg-open", "'", mntp ,"'" ])


    def close_encrypted(self, widget, data=None):
        #print "Closing encrypted volume"
        #print "Encrypted", self.entry_enc.get_text()
        #print "Mounted", self.entry_mnt.get_text()

        self.enc.close()

    def combo_text_changed(self, widgt, data=None):
        import os
        import shelve

        name = self.combo.get_active_text()
        #print "name =", name



        if os.path.exists(self.configfile):
            d = shelve.open(self.configfile)
            volumes = d['volumes']
            #print "volumes =", str(volumes)


            if volumes.has_key(name):
                data = volumes[name]
                enc = data['enc']
                mnt = data['mnt']
                password = data['password']
                self.entry_enc.set_text(enc)
                self.entry_mnt.set_text(mnt)
                self.entry_pass.set_text(password)

                if password !="":
                    # Mark the button save as active
                    self.check_save.set_active(gtk.TRUE)

    def save_data(self, widgt, data=None):

        import shelve
        d = shelve.open(self.configfile)

        if d.has_key('volumes'):
            volumes = d['volumes']
        else:
            volumes = {}

        name= self.combo.get_active_text()
        enc = self.entry_enc.get_text()
        mnt = self.entry_mnt.get_text()


        name = str(name)
        enc  = str(enc)
        mnt  = str(mnt)

        data = { 'enc': enc, 'mnt': mnt}

        if self.check_save.get_active():
            password = self.entry_pass.get_text()
            data['password'] = password
        else:
            data['password'] = ""

        volumes[name] = data

        d['volumes'] = volumes
        d.close()



if __name__ == "__main__":
    base = Base()
    base.main()