#!/bin/bash

SCRIPT=$0

usage () {
    echo "$SCRIPT [-h|--help] IPADDRESS [REMOTE_USER]";
    echo -en "\nRemove any known hosts keys and reconfigure "
    echo "passwordless SSH for the given IP address."
    exit 1;
}

ARGS=`getopt -o "h" -l "help" -n "reconfig_ssh.sh" -- "$@"`
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

echo "Reconfiguring SSH config for ${1}"
echo "Removing SSH known hosts entry..."
ssh-keygen -f "/home/sandc3/.ssh/known_hosts" -R ${1} 2>&1 |sed 's/^\(.*\)/\t\1/'
echo "OK"

echo -n "Reconfiguring Passwordless SSH "
if [[ $# -eq 2 ]]; then
    echo "for remote user $2..."
    ssh-copy-id ${2}@${1} 2>&1 |sed 's/^\(.*\)/\t\1/'
else
    echo "..."
    ssh-copy-id ${1} 2>&1 |sed 's/^\(.*\)/\t\1/'
fi
echo "OK"
exit 0
