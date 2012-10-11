#!/usr/bin/python

import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()

first_name = form.getvalue('first_name')
last_name = form.getvalue('last_name')


print "Content-Type:text/html\r\n\r\n"
print "<html><body>"
print "<h2>Results</h2>"
print "Thanks for playing %s %s" % (first_name, last_name)
print "<br/>See ya later."
print "</body></html>"
