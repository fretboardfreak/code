#!/bin/bash

SCRIPT=$0

usage () {
    echo "$SCRIPT [-h|--help] PATH";
    exit 1;
}

# Options with no args have no colon
# Option with required arg has 1 colon
# Option with optional arg has 2 colons
ARGS=`getopt -o "h" -l "help" -n "${0}" -- "$@"`
if [ $? -ne 0 ]; then
    # bad arguments found
    exit 1;
fi
eval set -- "$ARGS"

while true ; do
        case "$1" in
                -h|--help) usage ; shift ;;
                #-b|--b-long) echo "Option b, argument \`$2'" ; shift 2 ;;
                #-c|--c-long)
                #        # c has an optional argument. As we are in quoted mode,
                #        # an empty parameter will be generated if its optional
                #        # argument is not found.
                #        case "$2" in
                #                "") echo "Option c, no argument"; shift 2 ;;
                #                *)  echo "Option c, argument \`$2'" ; shift 2 ;;
                #        esac ;;
                --) shift ; break ;;
                *) echo "Internal error!" ; exit 1 ;;
        esac
done

path="${1}"
tmp_path="${1}.tmp"

cp -r ${path} ${tmp_path} && rm -r ${path} && mv ${tmp_path} ${path}
