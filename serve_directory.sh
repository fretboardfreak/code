#!/bin/bash

usage () {
    echo "$0 [PORT]"
    echo -en "\nServe the current working directory on given port. "
    echo -e "Port defaults to 8000."
    exit 0;
}

PORT=8000
if [[ $# -eq 1 ]]; then
    if [[ "${1:0:2}" == "-h" ]] || [[ "${1:0:3}" == "--h" ]]; then
        usage;
    fi
    PORT=$1
elif [[ $# -gt 1 ]]; then
    usage;
fi

python -m SimpleHTTPServer $PORT
