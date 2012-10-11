#!/usr/bin/env python
"""Webspring:  A wellspring for the web.
Converts a directory of markdown files into a website.

If outDir is not supplied, "_ws" is appended to the input directory name and
that is used as the output directory.  For example if the input directory is
"website" the output directory will be "website_ws".
"""
import sys, optparse, os, re, shutil

import mutagens.pandocMutagen as pandocMutagen

class WebspringException(Exception):
    pass

class Webspring:
    """Webspring converts a given directory into a website.
    """
    def __init__(self, inDir, outDir=None):
        self.inDir = self._sanitizePath(inDir)
        self.outDir = outDir
        self.filesToCopy = {}  # key:value = src:dest
        self.dirsToSpring = {} # key:value = src:dest

    def do(self):
        """call the high level actions that are needed to produce the website
        """
        self._setOutDir()
        self._checkEnvironment()
        self._springDir()
        self._copyFiles()
        self._springSubDirectories()

    def _copyFiles(self):
        """Copy the files from according to self.filesToCopy
        """
        for src, dest in self.filesToCopy.items():
            shutil.copy(src, dest)

    def _springDir(self):
        """
        """
        files = os.listdir(self.inDir)
        markdown = u'.*\.md$'
        ignore = u'(.*\.swp$|.*\.pyc$)'
        print "OutDir: %s" % self.outDir
        for inFile in files:
            inFname = os.path.join(self.inDir, inFile)
            outFname = self._calculateOutPath(inFname)
            if re.match(ignore, inFname):
                continue
            elif re.match(markdown, inFname):
                self._runPandoc(inFname, outFname)
            elif os.path.isdir(inFname):
                self.dirsToSpring[inFname] = outFname
            else:
                self.filesToCopy[inFname] = outFname

    def _runPandoc(self, inFname, outFname):
        """Run the pandoc mutagen on the given input and output file
        """
        outFname = self._mdNameToHtml(outFname)
        pandoc = pandocMutagen.PandocMutagen(inFname, outFname)
        pandoc.do()

    def _mdNameToHtml(self, fname):
        """Change the filename without changing the path
        """
        path, head = os.path.split(fname)
        parts = head.split('.')
        if parts[-1] in ['md']:
            parts[-1] = 'html'
        return os.path.join(path, '.'.join(parts))

    def _calculateOutPath(self, inPath):
        """Change the directory the file is in without changing the file name.

        This assumes the given inPath will be a subdirectory of self.inDir
        and every path has gone through self._sanitizePath already.
        """
        common = os.path.commonprefix([inPath, self.inDir])
        return os.path.join(self.outDir, inPath[len(common) + 1:])

    def _checkEnvironment(self):
        """Make sure expected paths exist and we can successfully move forward.
        """
        paths = [self.inDir, self.outDir]
        errMsg = "An expected path does not exist: %s"
        for path in paths:
            if not os.path.exists(path):
                raise WebspringException(errMsg % path)

    def _sanitizePath(self, path):
        return os.path.realpath(os.path.expanduser(path))

    def _setOutDir(self):
        """
        """
        if not self.outDir:
            path, dirName = os.path.split(self.inDir)
            self.outDir = self._sanitizePath(os.path.join(path, dirName + '_ws'))
        if not os.path.exists(self.outDir):
            os.makedirs(self.outDir)

    def _springSubDirectories(self):
        """Recursively create a Webspring instance for each subdirectory and call their do methods.
        """
        for inDir, outDir in self.dirsToSpring.items():
            webspring = Webspring(inDir, outDir)
            webspring.do()

## -- main --

def usage():
    return "Usage: Webspring.py [inDir] [outDir]"

def parseCmdLine():
    """
    manage cli invocation
    """
    parser = optparse.OptionParser( usage = usage(),
                           version = '%prog v0.1',
                           description = __doc__)
    return parser.parse_args()

def main():
    opts, args = parseCmdLine()

    if len(args) == 1:
        webspring = Webspring(args[0])
    elif len(args) == 2:
        webspring = Webspring(args[0], args[1])
    else:
        print usage()
        return 1

    webspring.do()
    return 0

if __name__ == '__main__':
    sys.exit(main())

