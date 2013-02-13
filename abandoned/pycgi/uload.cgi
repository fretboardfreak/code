#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()

FILEDIR="./files/"
form = cgi.FieldStorage()

# a nested FieldStorage instance holds the file
fileitem=form['file']

# Test if the file was uploaded
if fileitem.filename:
    # strip leading path from file name to avoid directory traversal attacks
    fn = os.path.basename(fileitem.filename)

    # make files dir if it doesn't exist
    if not os.path.isdir(FILEDIR):
        os.makedirs(FILEDIR)

    f = open(FILEDIR + fn, 'wb', 10000)

    # Read thefile in chunks
    chunk_size = 10000
    chunk = fileitem.file.read(chunk_size)
    while chunk:
        f.write(chunk)
        chunk = fileitem.file.read(chunk_size)
    f.close()
    message = 'The file "' + fn + '" was uploaded successfully'
else:
    message = 'No file was uploaded'

print """\
Content-Type: text/html\n
<html>
<head>
<meta http-equiv="REFRESH" content="0;url=http://curtissand.com/files/">
</head>
<body>
<p>%s</p>
</body></html>
""" % (message,)
