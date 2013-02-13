"""
"""

import cgitb
cgitb.enable()

import cgi, os, sys, logging
from cgiLib.baseInterface import BaseInterface

import markup

class FileViewInterface(BaseInterface):
    def __init__(self, filename, config, form, cookie):
        BaseInterface.__init__(self, form, cookie, config)
        self.fp = None
        self.filename = filename
        self.log = logging.getLogger('FileViewInterface')

    def run(self):
        self.log.info('running FileViewInterface')
        self.page.init(title=self.config.pageTitle,
                       css=self.config.css,
                       header=self._getNavBar(),
                       footer=self._getNavBar())
        self.addTitle()
        self.addContent()

    def addTitle(self):
        self.page.b()
        self.page.add(self.filename)
        self.page.b.close()

    def addContent(self):
        fp = open(os.path.join(self.config.contentDir, self.filename), 'r')
        content = cgi.escape(fp.read())
        fp.close()
        self.page.pre()
        self.page.add(content)
        self.page.pre.close()
