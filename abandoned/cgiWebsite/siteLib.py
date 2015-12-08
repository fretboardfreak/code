""" siteLib.py A library for use by various website focussed python scripts.
"""
import os, subprocess, time, re, sys

import config, markup, rst

def getPublicPath(path):
    common = os.path.commonprefix([path, config.CONTENT_DIR])
    return path[len(common):]

def validatePath(path):
    normalizedPath = os.path.normpath(os.path.join(config.CONTENT_DIR, path))
    if config.CONTENT_DIR != os.path.commonprefix([config.CONTENT_DIR, normalizedPath]):
        errMsg = ('The provided path points outside of the allowed content directory: ' +
                 'path=%s, normpath=%s' % (path, normalizedPath))
        log.error(errMsg)
        raise Exception(errMsg)

def getPath(form):
    path = '.'
    if form.has_key('path'):
        path = form.getvalue('path')
        validatePath(path)
    return path

def getFullPath(path, name=None):
    if not name:
        name = ''
    return os.path.normpath(os.path.join(config.CONTENT_DIR, path, name))

def getFileSystemInfo(path):
    """
        :return: {<fullPath>:{'property': 'value'}, ...}
    """
    info = {}
    if not os.path.isdir(path):
        info[path] = _getFileInfo(path)
        return info
    fnames = os.listdir(getFullPath(path))
    for name in fnames:
        if name.startswith('.'):
            continue
        target = getFullPath(path, name)
        if os.path.isdir(target):
            info[target] = _getDirectoryInfo(target)
        else:
            info[target] = _getFileInfo(target)
    return info

def _getDirectoryInfo(path):
    info = {}
    if not os.path.isdir(path):
        raise Exception('Cannot get directory info from a non-directory object: %s' % path)

    info.setdefault('type', 'dir')

    dirList = os.listdir(path)
    dirCount = fileCount = 0
    for fname in dirList:
        if os.path.isdir(os.path.join(path, fname)):
            dirCount += 1
        else:
            fileCount += 1
    info.setdefault('files', fileCount)
    info.setdefault('dirs', dirCount)
    info.setdefault('size', _getSize(path))
    return info

def _getSize(path):
    out, err, rc = runShellCommand('du -sh %s' % path)
    return out.split('\t')[0]

def _getFileInfo(path):
    # type, size, linecount, timestamp
    info = {}
    if os.path.isdir(path):
        raise Exception('Cannot get file stats from a directory: %s' % path)

    info.setdefault('type', _getFileType(path))
    info.setdefault('size', _getSize(path))
    info.setdefault('lines', _getLineCount(path))
    info.setdefault('accessed', _getTimestamp(path))

    return info

def _getTimestamp(path):
    seconds = os.path.getmtime(path)
    formatString = "%Y/%m/%d %H:%M:%S"
    return time.strftime(formatString, time.gmtime(seconds))

def _getFileType(path):
    out, err, rc = runShellCommand("/usr/bin/file -b %s" % path)
    return out.replace('\n', '')

# TODO: refactoring candidate
def runShellCommand(command):
    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()
    rc = process.returncode
    return out, err, rc

def _getLineCount(path):
    out, err, rc = runShellCommand("/usr/bin/wc -l %s" % path)
    return out.split(' ')[0]

def getNavBar(header=True):
    if not config.NAV_BAR:
        return ''
    navbar = markup.page()
    if not header:
        navbar.hr()
    navbar.ul(id='navlist')
    for text, url in config.NAV_BAR.iteritems():
        navbar.li(id='navlist')
        navbar.a(text, href=url)
        navbar.li.close()
    navbar.ul.close()
    if header:
        navbar.hr()
    return str(navbar)

def sortFileSystemInfos(fsInfo):
    fileInfos = {}
    dirInfos = {}
    for path, properties in fsInfo.iteritems():
        if properties['type'] == 'dir':
            dirInfos.setdefault(path, properties)
        else:
            fileInfos.setdefault(path, properties)
    return fileInfos, dirInfos

def extractContentGlobs(content):
    """ Turn text like "foo {{ref:link}} bar" into the dictionary {'ref':'link'}
    """
    pattern = '(?P<glob>{{.*:.*}})'
    matchIterator = re.finditer(pattern, content)
    globs = []
    while True:
        try:
            match = matchIterator.next()
        except StopIteration:
            break
        glob = match.group('glob')
        glob = glob.replace('{', '')
        glob = glob.replace('}', '')
        globType, value = glob.split(':')
        globs.append((globType, value, match.start(), match.end()))
    return globs

def handleContent(content, currentPath):
    """ Globs that look like {{key:value}} are meant for internal use, this
        function is where they are used.
    """
    supportedGlobTypes = ['ref', 'toc']
    basePath, _ = os.path.split(currentPath)
    globs = extractContentGlobs(content)
    sys.stderr.write('Globs = %s\n' % str(globs))
    for globType, value, start, end in globs:
        if globType not in supportedGlobTypes:
            continue
        if globType == 'ref':
            linkPath = os.path.normpath(os.path.join(basePath, value))
            validatePath(linkPath)
            fullLink = config.WEBSITE_URL + '?path=' + linkPath
            content = content[:start] + fullLink + content[end:]
        elif globType == 'toc':
            toc = getToc(currentPath, value)
            content = content[:start] + toc + content[end:]

    return rst.toHtml(content)

def getToc(currentPath, depth):
    """ Create a TOC in RST Format:

        .. sidebar:: Table of Contents

            - `filename <fullURL>`_
            - `filename2 <fullURL>`_
    """
    sys.stderr.write('Start TOC: Current path is: %s\n' % currentPath)
    toc = ".. sidebar:: Table of Contents\n\n"
    line = "    - `%s <%s>`_\n"
    directory, current = os.path.split(getFullPath(currentPath))
    dirList = os.listdir(directory)
    for filename in dirList:
        if filename == current:
            continue
        link = config.WEBSITE_URL + '?path=' + os.path.join(directory, filename)
        toc += line % (filename, link)
    return toc
