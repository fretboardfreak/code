#!/usr/bin/python
import sys

import config
from cgiLib.fileManagerSession import FileManagerSession

import logging
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
        filename='./fmanager.log')#'/dev/null')
log = logging.getLogger('fmanager.cgi')
log.info('*' * 40)

fms = FileManagerSession(config.contentDir)
fms.runSession()
