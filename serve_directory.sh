#!/bin/bash

usage () {
    echo "$0 [PORT]"
    echo -en "\nServe the current working directory on given port. "
    echo -e "Port defaults to 8000."
    exit 0;
}

PORT=8000
for arg in $@; do
    if [[ "${arg:0:2}" == "-h" ]] || [[ "${arg:0:3}" == "--h" ]]; then
        usage;
    fi
done

if [[ $# -eq 1 ]]; then
    PORT=$1
    DIR=
elif [[ $# -eq 2 ]]; then
    PORT=$1
    DIR=$2
elif [[ $# -gt 2 ]]; then
    usage;
fi

if [[ ! -z $DIR ]]; then
    cd $DIR
fi
python -m SimpleHTTPServer $PORT
