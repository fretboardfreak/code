#!/bin/bash

# $(($(date +%s) - $(stat --format "%X"  /proc/15473/cmdline)))

SCRIPT=$0

usage () {
    echo "$SCRIPT [-h|--help] PID";
    echo "Calculate the number of seconds a process has been running for."
    exit 1;
}

ARGS=`getopt -o "h" -l "help" -n "template.sh" -- "$@"`
if [ $? -ne 0 ]; then
    # bad arguments found
    exit 1;
fi
eval set -- "$ARGS"

while true ; do
        case "$1" in
                -h|--help) usage ; shift ;;
                --) shift ; break ;;
                *) echo "Internal error!" ; exit 1 ;;
        esac
done

if [[ $# -ne 1 ]]; then
    echo "$SCRIPT only expects a single parameter.";
    usage;
fi

pid=$1
if [[ ! -d /proc/$pid ]] || [[ ! -f /proc/$pid/cmdline ]]; then
    echo "Could not find '/proc/$pid' or '/proc/$pid/cmdline'."
    exit 1;
fi

echo $(($(date +%s) - $(stat --format "%X"  /proc/$pid/cmdline)))
