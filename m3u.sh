#!/bin/bash

SCRIPT=$0

# Turn on debug output
DEBUG=0

usage () {
    # Ruler 80 chars
    #       |--------------------------------------------------------------------------------|
    echo -e "Usage: $SCRIPT [-h|--help] [options] PLAYLIST FILES [FILES ...]"
    echo -e "\n  $SCRIPT creates, or appends to, an m3u format playlist file\n"
    echo -e "Options:"
    echo -e "  -h|--help                   : print this message"
    exit 1
};

parseOpts () {
    #echo -e "Args for parsOpts:\n$@\n"

    # Options with no args have no colon
    # Option with required arg has 1 colon
    # Option with optional arg has 2 colons
    ARGS=`getopt --options "dhi:p:r:" \
                 --long "help,interpreter:,prompt:,req-file:" \
                 --name "$SCRIPT" -- "$@"`

    if [ $? -ne 0 ]; then
        # bad arguments found
        usage;
        exit 1;
    fi
    eval set -- "$ARGS"

    while true ; do
        case "$1" in
            -h|--help) usage ; shift ; continue ;;
            -d) DEBUG=1 ; shift ;;
            --) shift ; break ;;
            *) echo "not recognized $1" ; exit 1 ;;
        esac
    done

    if [[ $# -ge 2 ]]; then
        PLAYLIST=$1
        shift
        FILES=$@
    else
        echo "Not enough arguments..."
        usage;
        exit 1
    fi
}

debug () {
    echo "Debug info:"
}

# ---- Main ----

parseOpts $@

if [[ DEBUG -eq 1 ]] ; then
    debug ;
fi

echo "Playlist file: \"$PLAYLIST\", Files: \"$FILES\""
for i in $FILES; do
    find $i -name '*.mp3' -type f >> $PLAYLIST
done
