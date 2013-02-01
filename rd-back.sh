#!/bin/bash

RDIFF="/usr/bin/rdiff-backup -v3"

LIVE_CLEAN="7D"
ARCHIVE_CLEAN="1Y"

HELP="rd-back.sh is a helper script for Fret's rdiff-backup needs.

The basic scheme is to make a live backup on a daily or hourly basis and then
on a less frequent cycle archive the backup to a second archive location.
This provides easy recovery of backups at a finer granularity but also
provides long term backups at a course granularity.  For my own purposes I
have found that this scheme reduces storage requirements while providing
sufficient granularity for recovery.\n
\n
Options: $ rd-back.sh [-h|-l|-a] SOURCE DEST\n
\n
    -h : print this help message\n
    -l : perform a backup and then clean increments older than '${LIVE_CLEAN}'\n
    -a : perform a backup and then clean increments older than '${ARCHIVE_CLEAN}'\n
"

function backup () {
    $RDIFF $1 $2
}

function clean () {
    $RDIFF --force --remove-older-than $1 $2
}

if [[ $1 == "-h" ]]; then
    exec echo -e $HELP
fi

if [[ $1 == -* ]] && [[ $# -eq 3 ]]; then
    if [[ $1 == "-l" ]]; then
        backup $2 $3
        clean $LIVE_CLEAN $3
    elif [[ $1 == "-a" ]]; then
        backup $2 $3
        clean $ARCHIVE_CLEAN $3
    fi
elif [[ $# -eq 2 ]]; then
    backup $1 $2
else
    exec echo -e $HELP
fi
