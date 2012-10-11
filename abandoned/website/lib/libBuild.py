""" The Builder Module holds the main Builder class and
    some other utilities for building a website.

    TODO:
"""
import os, sys, time, logging, StringIO
import pyLib.libMisc as libMisc
import pyLib.fsRecurser as fsRecurser
from pyLib.libContext import Redirect

import libPage

LOG = logging.getLogger('Builder')

VALID_SOURCE_TYPES=['.txt']

class FileMapper:
    def __init__(self, inputDir, outputDir):
        self.data = {}
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.replaceSuffix = lambda s, old, new: s[:s.rfind(old)] + new

    def visitFiles(self, current, files):
        commonIndex = len(os.path.commonprefix([self.inputDir, current]))
        LOG.info('FileMapper: current path = %s' % current)
        for fname in files:
            isValid = True in [fname.endswith(srcType) for srcType in VALID_SOURCE_TYPES]
            if not isValid:
                continue
            key = os.path.join(current, fname)
            value = os.path.join(self.outputDir, current[commonIndex:],
                                 self.replaceSuffix(fname, '.txt', '.html'))
            self.data.setdefault(key, value)

class Builder:
    """ Website builder
    """
    def __init__(self, config):
        self.config = config

    def build(self):
        """ Build the website. """
        LOG.info('Building Website...')
        self.fileMap = self._getSourceToOutputFileMap()
        for sourceFname, outputFname in self.fileMap.iteritems():
            if sourceFname.endswith('.txt'):
                page = libPage.toHtml(sourceFname, self.config)
            else:
                pass
            self._writeOutputFile(outputFname, str(page))

    def _writeOutputFile(self, filename, content):
        """ Write the content of an output file to the given filename. """
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        if os.path.exists(filename):
            LOG.info('output file %s exists... skipping!' % filename)
            return

        fp = None
        try:
            fp = open(filename, 'w')
            fp.write(content)
            LOG.info('wrote %s' % filename)
        finally:
            if fp:
                fp.close()

    def _getSourceToOutputFileMap(self):
        """ Create a mapping of source files to output files. """
        fileMapper = FileMapper(self.config.sourceDir, self.config.outputDir)
        recurser = fsRecurser.FSRecurser(self.config.sourceDir, fileMapper)
        recurser.recurse()
        return fileMapper.data

if __name__ == '__main__':
    print "This is a module library not a script"
    sys.exit(1)
