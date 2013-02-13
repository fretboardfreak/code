#!/usr/bin/python

import cgitb
cgitb.enable()

import cgi, os, sys, pickle, cgi
import markup

class UI:
    def __init__(self, title, contentDir, form):
        self.form = form
        self.title = title
        self.contentDir = contentDir
        self.page = None
        self.filename = None

    def execute(self):
        """
        """
        self.startPage()
        if self.form.has_key('filename'):
            self.filename = self.form.getvalue('filename')
        self.getFileList()
        self.printFile()

    def startPage(self):
        self.page = markup.page()
        self.page.init(title=self.title, css="./fret.css")
        self.page.small()
        self.page.a('Home', href='./blog.cgi')
        self.page.small.close()
        self.page.h1(self.title)

    def getFileList(self):
        fileList = os.listdir(self.contentDir)
        fileList.sort(reverse=True)
        if not self.filename:
            self.filename = fileList[0]
        currentFile = nextFile = prevFile = -1
        if self.filename in fileList:
            currentFile = fileList.index(self.filename)
            if currentFile > 0:
                nextFile = currentFile - 1
            if currentFile < len(fileList) - 1:
                prevFile = currentFile + 1

        self.page.form(action='./blog.cgi', method='get')
        self.page.select(name='filename')
        for filename in fileList:
            self.page.option(filename, value=filename)
        self.page.select.close()
        self.page.input(type='submit', value='Submit')
        self.page.form.close()

        if prevFile >= 0:
            self.page.a('Previous: ' + fileList[prevFile],
                        href='./blog.cgi?filename=%s' % fileList[prevFile])
        else:
            self.page.add('Previous: N/A')
        self.page.b()
        self.page.add('&nbsp;'*5 + self.filename + '&nbsp;'*5)
        self.page.b.close()
        if nextFile >= 0:
            self.page.a('Next: ' + fileList[nextFile],
                    href='./blog.cgi?filename=%s' % fileList[nextFile])
        else:
            self.page.add('Next: N/A')
        self.page.br()
        self.page.hr()

    def printFile(self):
        if not self.filename:
            return
        fullName = os.path.join(self.contentDir, self.filename)
        if not os.path.isfile(fullName):
            self.page.add('Could not find the given filename: %s' % self.filename)
            return
        fp = open(fullName, 'r')
        contents = fp.read()
        self.page.add(contents)

    def __str__(self):
        #return "Content-Type:text/html\r\n\r\n" + str(self.page)
        return str(self.page)

if __name__=="__main__":
    form = cgi.FieldStorage()
    ui = UI('Blog', './content/', form)
    ui.execute()

    print "Content-Type: text/html\r\n"
    print ui
