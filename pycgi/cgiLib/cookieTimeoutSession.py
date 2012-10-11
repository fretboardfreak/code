"""
CGI Session Manager

Provides a scheme for maintaining user sessions accross script executions in a CGI environment.
"""

import cgitb
cgitb.enable()

import cgi, Cookie, time, os, sys

from cgiLib.baseSession import BaseSession
from cgiLib.baseInterface import BaseInterface

class CookieTimeoutSession(BaseSession):
    def __init__(self):
        BaseSession.__init__(self)

    def runSession(self):
        self.cookie['date'] = time.time()
        interface = BaseInterface(self.form, self.cookie)
        interface.init(title='cookie test')
        if self.validCookie:
            interface.page.add('Using Existing Cookie')
        else:
            interface.page.add('No Cookie Found')
        print self.cookie
        print interface.getPage()
