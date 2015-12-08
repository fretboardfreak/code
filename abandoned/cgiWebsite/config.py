"""
Config Module for FretBoardFreak's CGI Website

Copyright 2012
"""

# PAGETITLE: Title of the Page used in markup.page's init function
PAGE_TITLE = "Development Page"

# css: css stylesheets
CSS = ["fret.css"]

# CONTENT_DIR: The absolute path to the content directory
#CONTENT_DIR = "/home/csand/blog"
#CONTENT_DIR = "/home/sandc3/public_html/content/"
CONTENT_DIR = "/home/sandc3/fret/"

# LOG_FILENAME: The relative path to the log file.
LOG_FILENAME = './cgi.log'

#WEBSITE_URL = "http://curtissand.com/test/index.cgi"
WEBSITE_URL = "http://webed.spgear.lab.emc.com/~sandc3/website/index.cgi"

# FILE_MANAGER_URL: URL for the File Manager CGI Interface
#FILE_MANAGER_URL = "http://curtissand.com/test/fileManager.cgi"
FILE_MANAGER_URL = "http://webed.spgear.lab.emc.com/~sandc3/website/fileManager.cgi"

NAV_BAR = {'File Manager': FILE_MANAGER_URL,
           'Home': WEBSITE_URL}

def validateConfig():
    checkRequired()
    checkContentDir()

def checkRequired():
    required = {'CONTENT_DIR': str,
                'PAGE_TITLE': str,
                'CSS': list,
                'LOG_FILENAME': str,
                'FILE_MANAGER_URL': str,
                'NAV_BAR': dict}

    for variable, kind in required.iteritems():
        if not isinstance(eval(variable), kind):
            msg = "Config Error: the variable '%s' of type %s not found." % \
                    (variable, kind)
            raise Exception(msg)

def checkContentDir():
    if not CONTENT_DIR.startswith('/'):
        msg = ("Config Error: variable 'contentDir'does not appear " +
               'to be absolute.  It does not start with "/".')
        raise Exception(msg)
