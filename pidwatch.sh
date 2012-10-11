#!/bin/bash

# Written by Curtis Sand, Sept. 2011

# TODO: this should be rewritten in python with some more options
#       like polling interval, type of notification, etc.

function usage() {
    echo "pidwatch.sh [-h] <pid>"
    echo "    Monitor the given pid.  When the process dies"
    echo "    notify the user via a popup message."
    echo "      -h - print this help message"
}

pid=
function pidwatch() {
    if [[ -z ${pid} ]]; then
        usage
    fi
    while [ true ]
    do
        ps --pid ${pid} > /dev/null
        val=$?
        if [[ ${val} -eq 1 ]]; then
            zenity --info --text "PID ${pid} appears to have stopped running"
            exit $?
        else
            # don't be too aggressive with the polling
            sleep 10
        fi
    done
}

function runTest() {
    while [ true ]
    do
        echo "blah"
    done
}

if [[ $# -eq 1 ]]; then
    if [[ ${1} = "-h" ]]; then
        usage
    fi
    pid=${1}
    pidwatch
else
    usage
fi
