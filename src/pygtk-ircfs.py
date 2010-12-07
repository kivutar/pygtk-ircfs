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
            f = open(path, 'r')
            gui.textbuffer.set_text(f.read())

    wm = WatchManager()
    notifier = Notifier(wm, PModify())
    wm.add_watch(path, IN_MODIFY)

    while 1:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()

class GUI():
    def __init__(self):
        self.tree = gtk.glade.XML('main.glade')
        self.window = self.tree.get_widget("mainWindow")
        self.textview = self.tree.get_widget("mainTextView")
        self.textbuffer = gtk.TextBuffer()
        self.textview.set_buffer(self.textbuffer)
        self.textbuffer.set_text('bar')
        self.window.connect("destroy", self.destroy)
        self.window.show_all()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.gdk.threads_init()
        gtk.gdk.threads_leave()
        gtk.main()
        gtk.gdk.threads_enter()
        gtk.gdk.flush()

if __name__ == '__main__':
    gui = GUI()
    guithread     = Thread(None, gui.main, None, (),                 {})
    monitorthread = Thread(None, Monitor,  None, (sys.argv[1], gui), {})
    monitorthread.start()
    guithread.start()
