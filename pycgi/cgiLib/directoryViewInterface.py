"""
"""

import cgitb
cgitb.enable()

import cgi, os, sys, logging
from cgiLib.baseInterface import BaseInterface

import markup

class DirectoryViewInterface(BaseInterface):
    def __init__(self, dirName, config, form, cookie):
        BaseInterface.__init__(self, form, cookie, config)
        self.dirName = dirName
        self.log = logging.getLogger('DirViewInterface')

    def getFullPath(self, name=None):
        if not name:
            name = ''
        return os.path.join(self.config.contentDir, self.dirName, name)

    def run(self):
        self.log.info('running interface')
        self.page.init(title=self.config.pageTitle,
                       css=self.config.css,
                       header=self._getNavBar(),
                       footer=self._getNavBar())
        self.addTitle()
        self.addContent()

    def addTitle(self):
        self.page.b()
        self.page.add('Current Working Directory: %s' % self.dirName)
        self.page.b.close()

    def getDirectoryInfo(self):
        dirInfo = {'directories':[], 'files': []}
        fnames = os.listdir(self.getFullPath())
        for name in fnames:
            if name.startswith('.'):
                continue
            path = self.getFullPath(name)
            if os.path.isdir(path):
                dirInfo['directories'].append(name)
            else:
                dirInfo['files'].append(name)
        [dirInfo[key].sort() for key in dirInfo.keys()]
        return dirInfo

    def getTarget(self, name):
        return os.path.join(self.dirName, name)

    def addContent(self):
        dirInfo = self.getDirectoryInfo()
        self.page.table()
        self.page.tr()
        self.page.td('Filename')
        self.page.td('Type')
        self.page.tr.close()
        for directory in dirInfo['directories']:
            target = self.getTarget(directory)
            self.page.tr()
            self.page.td()
            self.page.a(directory, href=self.config.fileManagerUrl+'?path='+target)
            self.page.td.close()
            self.page.td('Dir')
            self.page.tr.close()
        for fname in dirInfo['files']:
            target = self.getTarget(fname)
            self.page.tr()
            self.page.td()
            self.page.a(fname, href=self.config.fileManagerUrl+'?path='+target)
            self.page.td.close()
            self.page.td('File')
            self.page.tr.close()
        self.page.table.close()
