#!/bin/bash

SCRIPT=$0

usage () {
    echo "$SCRIPT [-h|--help|-b|--build] [BUILD_PATH]";
    echo -e "\n  Options:\n"
    echo "    -h|--help  :  Print this help message."
    echo "    -b|--build :  Build the cscope index files."
    local rc=0
    [ -n "$1" ] && rc=$1
    exit $rc
}

die () {
   echo $2
   exit $1
}

build () {
    if [[ ! -d $BUILD_PATH ]]; then
        die 1 "Build Path must be a directory."
    fi
    echo "Building Cscope for '$BUILD_PATH'"
    find $BUILD_PATH -iname "*.java" -o -iname "*.[ch]" \
                     -o -iname "*.cpp" -o -iname "*.cc" \
                     -o -iname "*.hpp" > $BUILD_PATH/cscope.files
    cscope -b -R -q -i $BUILD_PATH/cscope.files -f $BUILD_PATH/cscope.out
}
DO_BUILD=false
BUILD_PATH="$(pwd)"


ARGS=$(getopt -o "hb" -l "help,build" -n $SCRIPT -- "$@")
[ $? -ne 0 ] && usage 1  # bad arguments found
eval set -- "$ARGS"
while true ; do
    case "$1" in
        -h|--help) usage ; shift ;;
        -b|--build) DO_BUILD=true; shift ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done


if $DO_BUILD ; then
    if [[ $# -gt 1 ]] ; then
        echo "Build dir specified: $1"
        BUILD_PATH=$1
    fi
    build
fi
