#!/bin/bash

# Print Usage message to user
function usage {
    echo -en "tsrename.sh SUFFIX DIR"
    echo -en "\n\nRename all files in DIR by their last modification time."
    echo -en "\nFor SUFFIX, the '.' char is optional.\n\n"
    exit 1
}

# get the timestamp from the given file
function getFileDate {
    date -r $1 +%g%m%d-%H%M
}

# count how many files have the same name
function getFileCount {
    list=$(ls -1 $1*  2> /dev/null)
    if [[ $? -ne 0 ]]; then
        echo "_0"
    else
        echo "_`echo $list | wc -w`"
    fi
}

# make sure the suffix starts with '.'
function getDotSuffix {
    if [[ ${1:0:1} == "." ]]; then
        echo -ne $1
    else
        echo -ne ".$1"
    fi
}

# Remove the "./" prefix from the filename if it exists
function getFileName {
    if [[ ${1:0:2} == "./" ]]; then
        echo -ne ${1:2}
    else
        echo $1
    fi
}

if [[ $# -eq 2 ]]; then
    if [[ -d $2 ]]; then
        if [[ -z $1 ]]; then
            usage
        fi
        SUFFIX=$(getDotSuffix $1)
        DIR=$2
        pushd $DIR &> /dev/null
        echo "Renaming files in $DIR with suffix '$SUFFIX'..."
        for f in `find . -maxdepth 1 -name "*$SUFFIX"`; do
            file="$(getFileName $f)"
            fdate="$(getFileDate $file)"
            fname="${fdate}$(getFileCount $fdate)${SUFFIX}"
            echo "${file} -> ${fname}"
            mv ${file} ${fname}
        done
        popd &> /dev/null
    else
        usage
    fi
else
    usage
fi
