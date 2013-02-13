"""
File Manager Session
====================

A CGI interface for viewing, moving, removing and uploading files on the webserver.

Workflow
--------

.. note::

    All paths received from the webserver should only be used if they
    are both relative and contained within the contents directory.

- index.cgi
    Display the top level directory files only.

Form Values:
- path=relPath
    - If path is a file then display the File Page
    - if path is a directory then display the directory page
- action=someaction
    one of ['cp', 'rm', 'mv', 'ul', 'mkdir', 'rmdir']
        - 'cp' and 'mv' require 2 parameters "oldFile", "newFile"
        - 'ul' and 'mkdir' only require "newFile"
        - 'rm' and 'rmdir' only require "oldFile"
    when receive a full valid action then do the action and refresh
    the page with the path value in


"""

import cgitb
cgitb.enable()

import cgi, Cookie, time, os, sys, logging

from cgiLib.baseSession import BaseSession
from cgiLib.fileViewInterface import FileViewInterface
from cgiLib.directoryViewInterface import DirectoryViewInterface

import config

class FileManagerSession(BaseSession):
    def __init__(self, contentDir):
        BaseSession.__init__(self)
        if not contentDir.startswith('/'):
            msg = ('FileManagerSession: contentDir does not appear ' +
                   'to be absolute.  It does not start with "/".')
            raise Exception(msg)
        self.contentDir = contentDir
        self.path = None
        self.log = logging.getLogger('fileManSession')

    def runSession(self):
        self.log.info('Starting session.')
        self.setPath()
        self.getInterface()
        self.interface.run()
        print str(self.interface)
        sys.exit(0)

    def setPath(self):
        if self.form.has_key('path'):
            self.path = self.form.getvalue('path')
            self.validatePath()
        if not self.path:
            self.path = '.'
        self.log.info('Path has been set to: %s' % self.path)

    def getInterface(self):
        self.interface = None
        if os.path.isdir(os.path.join(config.contentDir, self.path)):
            self.log.info('Initializing DirectoryViewInterface')
            self.interface = DirectoryViewInterface(\
                    self.path, config, self.form, self.cookie)
        else:
            self.log.info('Initializing FileViewInterface')
            self.interface = FileViewInterface(\
                    self.path, config, self.form, self.cookie)

    def validatePath(self):
        normalizedPath = os.path.normpath(os.path.join(self.contentDir, self.path))
        if self.contentDir != os.path.commonprefix([self.contentDir, normalizedPath]):
            errMsg = ('The provided path points outside of the allowed content directory: ' +
                     'path=%s, normpath=%s' % (self.path, normalizedPath))
            self.log.error(errMsg)
            raise Exception(errMsg)


