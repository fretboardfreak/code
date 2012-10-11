"""
Config Module for FretBoardFreak's CGI Website

Copyright 2012
"""

# pageTitle: Title of the Page used in markup.page's init function
pageTitle = "Development Page"

# css: css stylesheets
css = ["fret.css"]

# contentDir: The absolute path to the content directory
#contentDir = "/home/csand/git/blog"
contentDir = "/home/sandc3/public_html/"

#fileManagerUrl = "http://www.curtissand.com/prv/blog/fmanager.cgi"
fileManagerUrl = "http://webed.spgear.lab.emc.com/~sandc3/cgi/fmanager.cgi"

navBar = {'File Manager':fileManagerUrl}
