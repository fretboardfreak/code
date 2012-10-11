#!/usr/bin/python
"""
CGI Based Website
"""
import os, cgi, sys

import markup
import rst
import config, cgiLib, siteLib

def noContentPage():
    page = markup.page()
    page.init(title=config.PAGE_TITLE,
              css=config.CSS,
              header=siteLib.getNavBar(header=True),
              footer=siteLib.getNavBar(header=False))
    page.b("Page not found. `Return to Main Page <%s>`_" % config.WEBSITE_URL)
    page.br()
    return page

def fileViewInterface(path, form, cookie):
    sys.stderr.write('file view interface path is: %s\n' % path)
    page = markup.page()
    page.init(title=config.PAGE_TITLE,
              css=config.CSS,
              header=siteLib.getNavBar(header=True),
              footer=siteLib.getNavBar(header=False))
    page.b()
    page.add(siteLib.getPublicPath(path))
    page.b.close()
    page.hr()
    if os.path.isdir(path):
        path = os.path.join(path, 'index.txt')
    if os.path.exists(path):
        fp = open(siteLib.getFullPath(path), 'r')
        content = fp.read()
        fp.close()
    else:
        return noContentPage()
    page.add(siteLib.handleContent(content, siteLib.getPublicPath(path)))
    #page.add(rst.toHtml(content))
    return page

def getPage(form, cookie):
    path = siteLib.getPath(form)
    if path == '.':
        path = 'index.txt'
    fullPath = siteLib.getFullPath(path)
    if not os.path.exists(fullPath):
        return noContentPage()
    return fileViewInterface(fullPath, form, cookie)

if __name__=="__main__":
    config.validateConfig()
    form, cookie = cgiLib.initCGI()
    page = getPage(form, cookie)
    sys.stderr.write('Testing stderr\n')
    cgiLib.sendPage(page)
