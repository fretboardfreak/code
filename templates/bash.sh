#!/bin/bash

# Print Usage
function usage () {
    echo "Usage info goes here"
}

# Script Scope Variables


# Function Definitions
function foo () {
    echo ""
}


# CMD Line Parsing and the body of the script
if [[ $# -eq 0 ]]; then
    foo
elif [[ $# -eq 1 ]]; then
    if [[ $1 = "-h" ]]; then
        usage
    else
        usage
    fi
else
    usage
fi

