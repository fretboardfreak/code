"""
CGI Session Manager

Provides a scheme for maintaining user sessions accross script executions in a CGI environment.
"""

import cgitb
cgitb.enable()

import cgi, os, sys


import markup

class BaseInterface:
    def __init__(self, form, cookie, config):
        self.form = form
        self.cookie = cookie
        self.config = config
        self.page = markup.page()

    def getFields(self):
        return []

    def init(self, *args, **kwargs):
        self.page.init(*args, **kwargs)

    def getPage(self):
        return str(self)

    def __str__(self):
        return "Content-Type: text/html\n\n" + str(self.page)

    def _getNavBar(self):
        if not self.config.navBar:
            return ''
        navbar = markup.page()
        navbar.ul(id='navlist')
        for text, url in self.config.navBar.iteritems():
            navbar.li(id='navlist')
            navbar.a(text, href=url)
            navbar.li.close()
        navbar.ul.close()
        return str(navbar)
