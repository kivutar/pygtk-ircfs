#!/usr/bin/env python

import os, sys
from time import sleep
import re
from threading import Thread
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

def Monitor(path, gui):
    while 1:
        #gui.treestore = gtk.TreeStore(str)
        #gui.treeview = gtk.TreeView(gui.treestore)
        #gui.populate(path)
        sleep(0.5)

class GUI():
    def __init__(self, path):
        self.path = path

        self.window = gtk.Window()
        self.window.set_title("List")

        self.treestore = gtk.TreeStore(str)
        self.treeview = gtk.TreeView(self.treestore)
        self.tvcolumn = gtk.TreeViewColumn('Servers')
        self.treeview.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.window.add(self.treeview)

        self.foo = {}
        self.populate(path)

        self.window.connect("destroy", self.on_destroy)
        self.treeview.connect("row-activated", self.on_row_activated)

        self.window.show_all()

    def populate(self, path=None, parentiter=None):
        for f in os.listdir(path):
            if not f in ['in', 'out']:
                currentiter = self.treestore.append(parentiter, [path+'/'+f])
            if os.path.isdir(path+'/'+f):
                self.populate(path+'/'+f, currentiter)

    def on_row_activated(self, widget, path=None, column=None):
        iter = self.treestore.get_iter(path)
        value = self.treestore.get_value(iter, 0)
        os.popen("./pygtk-ircfs.py " + value + " &")

    def on_destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.gdk.threads_init()
        gtk.gdk.threads_leave()
        gtk.main()
        gtk.gdk.threads_enter()
        gtk.gdk.flush()

if __name__ == '__main__':
    path = sys.argv[1]
    gui = GUI(path)
    guithread     = Thread(None, gui.main, None, (),          {})
    monitorthread = Thread(None, Monitor,  None, (path, gui), {})
    monitorthread.start()
    guithread.start()
