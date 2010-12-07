#!/usr/bin/env python

import os, sys
from threading import Thread
from pyinotify import *
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

def Monitor(path, gui):
    class PModify(ProcessEvent):
        def process_IN_MODIFY(self, event):
            f = open(path+'/out', 'r')
            gui.textbuffer.set_text(f.read())
            f.close()

    wm = WatchManager()
    notifier = Notifier(wm, PModify())
    wm.add_watch(path+'/out', IN_MODIFY)

    while 1:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()

class GUI():
    def __init__(self, path):
        self.path = path

        self.tree       = gtk.glade.XML('main.glade')
        self.window     = self.tree.get_widget("mainWindow")
        self.textview   = self.tree.get_widget("mainTextView")
        self.mainentry  = self.tree.get_widget("mainEntry")
        self.sendbutton = self.tree.get_widget("sendButton")

        self.textbuffer = gtk.TextBuffer()
        self.textview.set_buffer(self.textbuffer)
        self.textbuffer.set_text('bar')

        self.window.connect("destroy", self.destroy)
        self.sendbutton.connect("clicked", self.send)

        self.window.show_all()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def send(self, widget, data=None):
        message = self.mainentry.get_text()
        f = open(path+'/in', 'w')
        f.write(message+'\n')
        f.close()
        self.mainentry.set_text('')

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
