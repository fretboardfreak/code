#!/bin/bash

usage () {
    echo -en "$0 [INTERFACE]"
    echo -en "\nRetrieve the IP address assigned to the given interface. "
    echo -e "Default interface is eth0"
    exit 0;
}

INTERFACE=eth0
if [[ $# -eq 1 ]]; then
    if [[ "${1:0:2}" == "-h" ]] || [[ "${1:0:3}" == "--h" ]]; then
        usage;
    fi
    INTERFACE=$1;
elif [[ $# -gt 1 ]]; then
    usage;
fi

ip addr show dev $INTERFACE | grep inet | grep -v inet6 |\
    sed -e 's/^ \+inet //g' -e 's/\/[0-9]\+ brd.*$//g'
