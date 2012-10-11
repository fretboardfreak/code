#!/usr/bin/env python

#google-chrome --app="`zenity --list --text=Choose\ a\ Bookmark --column=ID --column=Name --column=URL --print-column=3 1 gmail https://gmail.google.com 2 wired www.wired.com`"

import subprocess as sp

bookmarks = [
    'Custom URL',   'custom',
    'GCal',         'http://www.google.com/calendar',
    'GMail',        'https://mail.google.com',
    'GReader',      'http://google.com/reader',
    'GDocs',        'https://docs.google.com',
    'FBF Wiki',     'http://curtissand.com/blog',
    'FBF New Post', 'http://curtissand.com/blog/wp-admin/press-this.php',
    'Zorg Empire',  'http://www.zorgempire.com/index.php',
    'Eternaverse',  'http://uni1.eternaverse.org/index.php',
    'Wikipedia',    'http://en.wikipedia.org/wiki/Main_Page',
    'Kongregate',   'http://www.kongregate.com/',
    'GrooveShark',  'http://listen.grooveshark.com',
    ]
zenityCmd = ['zenity', '--list', '--text=Choose\ a\ Bookmark\ to\ Appify',
             '--column=Name', '--column=URL', 
             '--print-column=2', '--hide-column=2',
             '--width=100', '--height=400'
             ]
zenityCmd.extend(bookmarks)

zenity = sp.Popen(zenityCmd, stdout=sp.PIPE)

zenityResult, _ = zenity.communicate()

if zenityResult == 'custom\n':
    zenityCmd = ['zenity', '--entry',
                 '--text=Enter\ URL\ to\ Open\ Fullscreen\ in Google\ Chrome']
    zenity = sp.Popen(zenityCmd, stdout=sp.PIPE)
    zenityResult, _ = zenity.communicate()

if not zenityResult:
    exit(1)
if zenityResult[-1] == '\n':
    zenityResult = zenityResult[:-1]


googleChromeCmd = ['/usr/bin/google-chrome', '--app=%s' % zenityResult]

sp.Popen(googleChromeCmd)

exit(0)
