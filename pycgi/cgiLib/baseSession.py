"""
CGI Base Session Manager

Provides a scheme for maintaining user sessions accross script executions in a CGI environment.
"""

import cgitb
cgitb.enable()

import cgi, Cookie, time, os

from cgiLib.baseInterface import BaseInterface

class BaseSession:
    def __init__(self):
        self.cookieTimeout = 10 #14400 # 4 hours in seconds
        self.cookieFields = ['date']
        self.formFields = []
        self.cookie = Cookie.SimpleCookie()
        self.validCookie = self.getCookie()
        self.form = cgi.FieldStorage()

    def getCookie(self):
        """ Load the cookie if it is both available and valid.
        Only return True if there is a valid cookie that has not yet expired.
        """
        if self.loadCookie():
            date = self.cookie.get('date')
            if date:
                date = float(date.value)
                if time.time() - date <= self.cookieTimeout:
                    return True
        return False

    def loadCookie(self):
        """ If the webserver has a cookie for us then load it.
        """
        if os.environ.has_key('HTTP_COOKIE'):
            self.cookie.load(os.environ['HTTP_COOKIE'])
            return True
        return False

    def runSession(self):
        raise NotImplementedError()
