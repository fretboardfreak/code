#!/bin/bash

if [[ `hostname` = sandc3 ]]
then
    echo "Running backup on host `hostname`"
    SOURCE_DIR="/local/sandc3/"
    SOURCES="fret config code blog notes"
    DEST_DIR="/local/nobackup/backups/"
elif [[ `hostname` = shiny ]]
then
    echo "Running backup on host `hostname`"
    SOURCE_DIR="/home/csand/"
    SOURCES="fret config code blog"
    DEST_DIR="/home/csand/backups/"
else
    echo "No backup config for host `hostname`"
    exit 1
fi

RDIFF="/usr/bin/rdiff-backup -v3"

LIVE_SUFFIX=".bak"
LIVE_REMOVE_OLDER_THAN="7D"

ARCHIVE_SUFFIX=".arch"
ARCHIVE_REMOVE_OLDER_THAN="1Y"

function usage () {
    echo "Usage:/> backup [option]"
    echo "    -h : show this message"
    echo "    -l : perform a live backup"
    echo "    -a : perform an archive"
    echo "    -cl : cleanup live backups older than '$LIVE_REMOVE_OLDER_THAN'"
    echo "    -ca : cleanup archives older than '$ARCHIVE_REMOVE_OLDER_THAN'"
}

if [[ $# -eq 1 ]]
then
    if [[ $1 == '-h' ]] # print options
    then
        usage
    elif [[ $1 == '-l' ]] # do live backup
    then
        for x in $SOURCES;
        do
            ${RDIFF} ${SOURCE_DIR}${x} ${DEST_DIR}${x}${LIVE_SUFFIX}
        done
    elif [[ $1 == '-a' ]] # do archive backup
    then
        for x in $SOURCES;
        do
            ${RDIFF} ${SOURCE_DIR}${x} ${DEST_DIR}${x}${ARCHIVE_SUFFIX}
        done
    elif [[ $1 == '-cl' ]] # cleanup live mirror
    then
        for x in $SOURCES;
        do
            ${RDIFF} --force --remove-older-than ${LIVE_REMOVE_OLDER_THAN} ${DEST_DIR}${x}${LIVE_SUFFIX}
        done
    elif [[ $1 == '-ca' ]] # cleanup archive mirror
    then
        for x in $SOURCES;
        do
            ${RDIFF} --force --remove-older-than ${ARCHIVE_REMOVE_OLDER_THAN} ${DEST_DIR}${x}${ARCHIVE_SUFFIX}
        done
    else
        usage
    fi
else
    usage
fi
