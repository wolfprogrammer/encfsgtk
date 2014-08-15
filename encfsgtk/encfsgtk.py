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

import os
import signal
import logging
import logging.config

LOG_ENABLE = False
LOG_LEVEL   = 'WARNING' # 'WARNING', 'INFO', 'CRITICAL', 'NOTSET', 'ERROR',

LOG_SETTINGS = {
    # --------- GENERAL OPTIONS ---------#
    'version': 1,
    'disable_existing_loggers': False,

    # ---------- LOGGERS ---------------#
    'root': {
        'level': LOG_LEVEL,
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
    # Will create the log file
    logging.config.dictConfig(LOG_SETTINGS)
    log = logging.getLogger("root")
else:
    # All logs will be disabled
    log = logging.getLogger()
    logging.disable(logging.CRITICAL)




log.info("==== starting Encfsgtk logging =====")




from encfs import Encfs



def erro_mbox(erro_message, parent=None):
    message = gtk.MessageDialog(parent=parent,type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
    message.set_markup(erro_message)
    message.run()

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

def msgbox_error( msg, title = "gtkBuilder Selector"):
    import gtk

    dlg = gtk.MessageDialog( type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_CLOSE )
    dlg.set_title( title )
    dlg.set_markup( msg )
    dlg.run()
    dlg.destroy()

def msgbox_ok(msg, title):
    import gtk

    dlg = gtk.MessageDialog( type = gtk.MESSAGE_INFO, buttons = gtk.BUTTONS_OK )
    dlg.set_title( title )
    dlg.set_markup( msg )
    dlg.run()
    dlg.destroy()

class Base:
    """
    Main window class
    """

    def __init__(self):

        log.info("Starting main window")

        import os
        self.configfile = os.path.expanduser('~/.encfsgui.db')

        self.user_process = None

        #self.configfile = "~/encfsgui.db"

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        #self.window.set_size_request(500, 500)
        self.window.set_title("EncfsGtk")
        self.window.connect("destroy", self.destroy)

        import tempfile
        import base64
        icondata = "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"


        with  tempfile.NamedTemporaryFile(suffix=".png", delete=True) as temp:
            log.debug("Creating temporary file")

            icon = temp.name

            log.debug("icon = %s" % icon)

            fp = open(icon, "wb")
            fp.write(base64.b64decode(icondata))
            fp.close()
            self.window.set_icon_from_file(icon)
        #self.window.set_icon_from_file("icon.png")

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
        self.label4 = gtk.Label("Command after opened")

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

        # Command entry
        self.entry_cmd_opened = gtk.Entry()
        self.entry_cmd_opened.set_tooltip_text("Command to be executed after the volume be opened")



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

        self.button_remove = gtk.Button("Remove")
        self.button_remove.set_tooltip_text("Remove volume from list, but don't delete it.")
        self.button_remove.connect("clicked", self.remove_data)


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
        self.label4.set_alignment(0, 0.5)

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

        hbox7 = gtk.HBox(spacing=10, homogeneous=True)
        hbox7.pack_start(self.label4)
        hbox7.pack_start(self.entry_cmd_opened)

        vbox1 = gtk.VBox(spacing=10)
        vbox1.pack_start(self.check1)
        vbox1.pack_start(self.check_reverse)
        vbox1.pack_start(self.check_save)

        hbox4 = gtk.HBox(spacing=10, homogeneous=True)
        hbox4.pack_start(self.button_mount)
        hbox4.pack_start(self.button_umount)

        hbox5 = gtk.HBox(spacing=10, homogeneous=True)
        hbox5.pack_start(self.button_save)
        hbox5.pack_start(self.button_remove)

        hbox6 = gtk.HBox(spacing=10, homogeneous=True)
        hbox6.pack_start(self.button_exit)



        vbox.pack_start(hbox0)
        vbox.pack_start(hbox1)
        vbox.pack_start(hbox2)
        vbox.pack_start(hbox7)
        vbox.pack_start(hbox3)
        vbox.pack_start(vbox1)
        vbox.pack_start(hbox4)
        vbox.pack_start(hbox5)
        vbox.pack_start(hbox6)

        self.window.add(vbox) # Add fixed container to main window
        # Show main window



    def main(self):
        log.info("Entering window main loop")
        gtk.main()

    #----------- GUI Signals -------------- #

    def destroy(self, widget, data=None):
        """
        Kill the app when the app is closed
        """
        #print "App closed"

        if self.user_process is not None:
            pid = self.user_process.pid
            os.killpg(pid, signal.SIGTERM)

        self.enc.close()

        log.info("Quit application")
        gtk.main_quit()

    def open_encrypted(self, widget, data=None):

        from subprocess import Popen, PIPE

        log.info("Opening encrypted volume")
        #print "Mounting encrypted volume"
        #print "Encrypted", self.entry_enc.get_text()
        #print "Mounted", self.entry_mnt.get_text()

        encp = self.entry_enc.get_text()
        mntp = self.entry_mnt.get_text()
        password = self.entry_pass.get_text()
        cmdo = self.entry_cmd_opened.get_text()

        log.debug({'encp':encp, 'mntp':mntp, 'password': password, 'cmdo': cmdo})

        if password == "":
            return

        self.enc = Encfs()
        status = self.enc.open(encp, mntp, password)

        log.debug("status : %s" % status)

        if not status:
            msgbox_error("Error: Wrong password.","ERRO")

            return
        else:
            msgbox_ok("Password OK!", "INFO")

        if cmdo !="":
            self.user_process = Popen(cmdo, shell=True, preexec_fn=os.setsid)
            #log.debug("self.user_process.pid = " %  self.user_process.pid)

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
        log.info("Closing encrypted volume")

        # Clean password if save-password not check
        if not self.check_save.get_active():
            self.entry_pass.set_text("")


        if self.user_process is not None:

            pid = self.user_process.pid
            os.killpg(pid, signal.SIGTERM)
            #self.user_process.kill()

        self.enc.close()

    def combo_text_changed(self, widgt, data=None):
        import os
        import shelve

        log.info("Text changed")

        name = self.combo.get_active_text()

        log.debug("name: %s" % name)

        if os.path.exists(self.configfile):
            log.debug("Exists configfile = %s " % self.configfile)


            d = shelve.open(self.configfile)
            volumes = d['volumes']

            log.debug("volumes = %s" % volumes)

            #print "volumes =", str(volumes)

            #print "p1"

            # Repopulate combox
           # entries = volumes.keys()

            #for e in entries:
            #    self.combo.append_text(e)


            if volumes.has_key(name):
                data = volumes[name]
                enc = data['enc']
                mnt = data['mnt']
                password = data['password']
                cmdo = data['cmdo']

                log.debug({'data': data, 'enc': enc, 'mnt': mnt, 'password': password, 'cmdo': cmdo})


                self.entry_enc.set_text(enc)
                self.entry_mnt.set_text(mnt)
                self.entry_pass.set_text(password)
                self.entry_cmd_opened.set_text(cmdo)
                self.enc = Encfs()
                self.enc.open(enc, mnt, password, mount=False)

                if password !="":
                    # Mark the button save as active
                    self.check_save.set_active(gtk.TRUE)

            else:
                self.entry_enc.set_text("")
                self.entry_mnt.set_text("")
                self.entry_pass.set_text("")
                self.entry_cmd_opened.set_text("")


    def save_data(self, widgt, data=None):

        log.info("Saving data")

        import shelve
        d = shelve.open(self.configfile)

        if d.has_key('volumes'):
            volumes = d['volumes']
        else:
            volumes = {}

        name= self.combo.get_active_text()
        enc = self.entry_enc.get_text()
        mnt = self.entry_mnt.get_text()
        cmdo = self.entry_cmd_opened.get_text()
        
        name = str(name)
        enc  = str(enc)
        mnt  = str(mnt)
        cmdo = str(cmdo)

        data = { 'enc': enc, 'mnt': mnt, 'cmdo': cmdo}

        if self.check_save.get_active():
            password = self.entry_pass.get_text()
            data['password'] = password
        else:
            data['password'] = ""

        volumes[name] = data

        d['volumes'] = volumes
        d.close()

    def remove_data(self, widgt, data=None):

        import shelve
        d = shelve.open(self.configfile)

        if d.has_key('volumes'):
            volumes = d['volumes']
        else:
            return

        name= self.combo.get_active_text()
        #if volumes.has_key(name):
        #    volumes.remove(name)

        try:
            del volumes[name]
        except:
            pass

        d['volumes'] = volumes
        d.close()

def main():
    base = Base()
    base.main()

if __name__ == "__main__":
    main()