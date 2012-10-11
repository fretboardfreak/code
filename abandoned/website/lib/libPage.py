""" libPage provides module level functions for building RST files into HTML
    pages.
"""
import logging
import pyLib.rst as rst
import external.markup as markup

LOG = logging.getLogger('Page')

def _readFile(source):
    content = None
    try:
        fp = open(source, 'r')
        content = fp.read()
    finally:
        fp.close()
    return content

def toHtml(source, config):
    page = markup.page()
    page.init(title=config.title,
              script=config.script)
              #header=siteLib.getNavBar(header=True),
              #footer=siteLib.getNavBar(header=False))

    errFp = StringIO.StringIO()
    with Redirect(stderr=errFp):
        page.add(rst.toHtml(_readFile(source)))
    errors = errFp.getvalue()
    if errors != "":
        msg = "Errors encountered:\n%s" % errors
        LOG.error(msg)
        raise Exception(msg)

    return page
    #page.add(siteLib.handleContent(content, siteLib.getPublicPath(path)))
