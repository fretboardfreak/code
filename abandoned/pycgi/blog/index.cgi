#!/usr/bin/python

import cgitb
cgitb.enable()

import cgi
from ui import UI

form = cgi.FieldStorage()
ui = UI('Blog', '/home/sandc3/fret/', form)
ui.execute()

print "Content-Type: text/html\r\n"
print ui
