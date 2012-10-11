""" cgiLib.py : A library of helper functions for CGI scripts.
"""
import logging, cgitb, cgi, Cookie, time, os

import config

def initLogging(logFilename):
    """ Initialize the logging module.
    """
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s: %(levelname)s: %(message)s',
            filename=logFilename)#'/dev/null')

def initCGI():
    """ Initialize basic CGI environment
    """
    cgitb.enable()
    return (cgi.FieldStorage(), getCookie())

def getCookie(cookieTimeout=14400):
    cookie = Cookie.SimpleCookie()
    if loadCookie(cookie):
        date = cookie.get('date')
        if date:
            date = float(date.value)
            if time.time() - date <= cookieTimeout:
                return cookie

def loadCookie(cookie):
    envVar = 'HTTP_COOKIE'
    if os.environ.has_key(envVar):
        cookie.load(os.environ[envVar])
        return True
    return False

def sendPage(page):
    msg = "Content-type: text/html\r\n\n" + str(page)
    print msg
