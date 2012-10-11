#!/bin/sh

CELLPATH=/media/CSANDROID/

echo "Syncing fret..."
unison -perms 0o0 -batch -terse ~/fret/ ${CELLPATH}fret/

echo "Syncing code..."
unison -perms 0o0 -batch -terse ~/code/ ${CELLPATH}code/

echo "Syncing config..."
unison -perms 0o0 -batch -terse ~/config/ ${CELLPATH}config/

#echo "Syncing backups..."
#unison -perms 0o0 -batch -terse /local/nobackup/backups/ ${CELLPATH}backups/
