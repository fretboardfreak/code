#!/usr/bin/env python
"""This module contains the PandocMutagen class.
"""
import subprocess, sys

from baseMutagen import BaseMutagen

class PandocMutagenException(Exception):
    pass

class PandocOptions:
    """A simple options class for configuring a PandocMutagen
    """
    def __init__(self, **kwargs):
        """Setup defaults if they aren't already in kwargs.  Ignore invalid options.
        """
        # options
        self.read         = kwargs.setdefault('read', 'markdown')
        self.write        = kwargs.setdefault('write', 'html')
        self.output       = kwargs.setdefault('output', '-')
        self.id_prefix    = kwargs.setdefault('id-prefix', '')
        self.css          = kwargs.setdefault('css', 'style.css')
        self.title_prefix = kwargs.setdefault('title-prefix', '')
        self.email_obfuscation = kwargs.setdefault('email-obfuscation', 'javascript')

        # flags
        self.standalone        = kwargs.setdefault('standalone', True)
        self.smart             = kwargs.setdefault('smart', False)
        self.incremental       = kwargs.setdefault('incremental', False)
        self.number_sections   = kwargs.setdefault('number-sections', False)
        self.no_wrap           = kwargs.setdefault('no-wrap', False)
        self.table_of_contents = kwargs.setdefault('table-of-contents', True)

        self._setTables()

    def _setTables(self):
        """list of valid options and flags for the iterator
        """
        self.OPTIONS = {
                'read': self.read,
                'write': self.write,
                'output': self.output,
                'id-prefix': self.id_prefix,
                'css': self.css,
                'title-prefix': self.title_prefix,
                'email-obfuscation': self.email_obfuscation
                }

        self.FLAGS = {
                'standalone': self.standalone,
                'smart': self.smart,
                'incremental': self.incremental,
                'number-sections': self.number_sections,
                'no-wrap': self.no_wrap,
                'table-of-contents': self.table_of_contents,
                }

    def __iter__(self):
        self._setTables()
        items = self.OPTIONS.items()
        items.extend(self.FLAGS.items())
        return items.__iter__()

    def __str__(self):
        self._setTables()
        cmdStr = ''
        for name, opt in self:
             if name in self.OPTIONS.keys():
                 if (name in ['id-prefix', 'title-prefix']) and opt == '':
                     continue
                 cmdStr += '--%s %s ' % (name, opt)
             elif opt and (name in self.FLAGS.keys()):
                 cmdStr += '--%s ' % name
        return cmdStr

class PandocMutagen(BaseMutagen):
    """Provide a simple interface to the pandoc markup translation tool.
    """
    def __init__(self, inFname = '', outFname = '', options = PandocOptions(),
                 executable = '/usr/bin/pandoc'):
        self.inFname = inFname
        self.outFname = outFname
        self.executable = executable
        self.options = options
        self.options.output = self.outFname

    def do(self):
        """ run the mutagen to create an effect
        """
        command = '%s %s %s' % (self.executable, self.options, self.inFname)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stdout:
            sys.stdout.write(stdout + '\n')
        if stderr:
            raise PandocMutagenException('Error processing %s: %s' % (self.inFname, stderr))
        result = 'failure'
        if proc.returncode == 0:
            result = 'success'
        sys.stdout.write('Processed File: %s: %s\n' % (self.inFname, result))

## Functions for direct use of this module
def usage():
    print "Usage: pandocMutagen.py [inFname] [outFname]"

def sanitizePath(path):
    return os.path.realpath(os.path.expanduser(path))

def main(argv):
    argv.pop(0)
    if len(argv) != 2:
        usage()
        return 1
    inFname = sanitizePath(argv[0])
    outFname = sanitizePath(argv[1])
    mutagen = PandocMutagen(inFname, outFname)
    mutagen.do()
    return 0

if __name__=="__main__":
    import os.path
    sys.exit(main(sys.argv))

