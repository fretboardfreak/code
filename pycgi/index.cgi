#!/usr/bin/python

import config
from cgiLib.rstSession import RstSession

import logging
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',
        filename='./fmanager.log')#'/dev/null')
log = logging.getLogger('fmanager.cgi')
log.info('*' * 40)

rst = RstSession()
rst.runSesion()
