#!/usr/bin/env python

import os, sys
from time import sleep
from threading import Thread
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

def Monitor(path, gui):
    oldmtime = None
    while 1:
        sleep(0.1)
        newmtime = os.stat(path+'/out')[8]
        if newmtime != oldmtime:
            f = open(path+'/out', 'r')
            gui.textbuffer.set_text(f.read())
            f.close()
            gui.scrolltoend()
        oldmtime = newmtime

class GUI():
    def __init__(self, path):
        self.path = path

        self.tree           = gtk.glade.XML('main.glade')
        self.window         = self.tree.get_widget("mainWindow")
        self.scrolledwindow = self.tree.get_widget("mainScrolledWindow")
        self.textview       = self.tree.get_widget("mainTextView")
        self.mainentry      = self.tree.get_widget("mainEntry")
        self.sendbutton     = self.tree.get_widget("sendButton")

        self.textbuffer = gtk.TextBuffer()
        self.textview.set_buffer(self.textbuffer)
        self.textbuffer.set_text('bar')

        self.window.connect("destroy", self.on_destroy)
        self.sendbutton.connect("clicked", self.on_send)

        self.window.show_all()
        self.scrolltoend()

    def on_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_send(self, widget, data=None):
        message = self.mainentry.get_text()
        self.send_message(message)
        self.mainentry.set_text('')

    def send_message(self, message):
        f = open(path+'/in', 'w')
        f.write(message+'\n')
        f.close()

    def scrolltoend(self):
        print "scroooollll"
        adjustment = self.scrolledwindow.get_vadjustment()
        upper = adjustment.get_upper()
        print upper
        adjustment.set_value(upper)

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
