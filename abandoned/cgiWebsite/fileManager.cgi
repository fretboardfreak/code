#!/usr/bin/python
"""
CGI Based File Manager
"""
import os, cgi

import markup
import config, cgiLib, siteLib

def getInterface(path):
    interface = None
    if os.path.isdir(os.path.join(config.CONTENT_DIR, path)):
        interface = directoryViewInterface
    else:
        interface = fileViewInterface
    return interface

def fileViewInterface(path, form, cookie):
    page = markup.page()
    page.init(title=config.PAGE_TITLE,
              css=config.CSS,
              header=siteLib.getNavBar(),
              footer=siteLib.getNavBar())
    page.b()
    page.add(path)
    page.b.close()
    fp = open(os.path.join(config.CONTENT_DIR, path), 'r')
    content = cgi.escape(fp.read())
    fp.close()
    page.pre()
    page.add(content)
    page.pre.close()
    return page

def directoryViewInterface(path, form, cookie):
    page = markup.page()
    page.init(title=config.PAGE_TITLE,
              css=config.CSS,
              header=siteLib.getNavBar(),
              footer=siteLib.getNavBar())

    fsInfo = siteLib.getFileSystemInfo(path)
    fileInfos, dirInfos = siteLib.sortFileSystemInfos(fsInfo)

    page.b()
    page.h1(config.PAGE_TITLE)
    page.add("Viewing '%s'" % path)
    page.b.close()
    page.br()
    page.add(getDirectoryTable(dirInfos))
    page.add(getFileTable(fileInfos))
    return page

def getFileTable(fileInfos):
    """
    fileInfos = {<path>: {'accessed':'X','lines': 'X','size': 'X','type': 'X'}, ...}
    """
    headings = {'accessed': 'Last Accessed', 'lines': 'Line Count', 'size': 'Size', 'type': 'Filetype'}
    page = markup.page()
    page.table()

    page.tr()
    page.td('File')
    [page.td(heading) for heading in headings.values()]
    page.tr.close()
    for path, properties in fileInfos.iteritems():
        _, fname = os.path.split(path)
        page.tr()
        page.td()
        page.a(fname, href=config.FILE_MANAGER_URL+'?path='+path)
        page.td.close()
        [page.td(properties[key]) for key in headings.keys()]
        page.tr.close()

    page.table.close()
    return str(page)

def getDirectoryTable(dirInfos):
    """
    dirInfos = {<path>: {'dirs': X, 'files': X, 'size': 'X', 'type': 'dir'}, ...}
    """
    headings = {'files':'File Count', 'dirs': 'Dir. Count', 'size': 'Size'}
    page = markup.page()
    page.table()

    page.tr()
    page.td('Directory')
    [page.td(heading) for heading in headings.values()]
    page.tr.close()
    for path, properties in dirInfos.iteritems():
        properties.pop('type')
        _, fname = os.path.split(path)
        page.tr()
        page.td()
        page.a(fname, href=config.FILE_MANAGER_URL+'?path='+path)
        page.td.close()
        [page.td(properties[key]) for key in headings.keys()]
        page.tr.close()

    page.table.close()
    return str(page)

if __name__=="__main__":
    config.validateConfig()
    form, cookie = cgiLib.initCGI()
    path = siteLib.getPath(form)
    interface = getInterface(path)
    page = interface(path, form, cookie)
    cgiLib.sendPage(page)
