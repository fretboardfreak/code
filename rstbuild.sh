#!/bin/bash
# Copyright 2016 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
SCRIPT=$0

STYLESHEET="${HOME}/code/css/rstskel.css,${HOME}/code/css/normalize.css"
SUFFIX="rst"
RST_OPTS="--cloak-email-addresses --embed-stylesheet"
RST2HTML=$(which rst2html.py)
CLEAN=false

usage () {
    echo "$SCRIPT [options] TOP_DIR";
    echo -e "\nRecursively build a directory of RST files into HTML."
    echo -e "\nOptions:"
    echo "  -h|--help        Print this help message."
    echo "  -s|--stylesheet  Use a different stylesheet."
    echo "                   [Default: $STYLESHEET]"
    echo "  --suffix         Read RST files using a different suffix."
    echo "                   [Default: $SUFFIX]"
    echo "  --rst-options    Use a different set of options for \"$RST2HTML\"."
    echo "                   Note; stylesheets are customized using "
    echo "                         the -s|--stylesheet flag."
    echo "                   [Default: $RST_OPTS]"
    echo "  -c|--clean          Clean up the md5 and html files in the target."
    local rc=0
    [ -n "$1" ] && rc=$1
    exit $rc
}

ARGS=$(getopt -o "hs:c" -l "help,stylesheet:,suffix:,rst-options:,clean" -n $SCRIPT -- "$@")
[ $? -ne 0 ] && usage 1  # bad arguments found

eval set -- "$ARGS"
while true ; do
    case "$1" in
        -h|--help) usage ; shift ;;
        -s|--stylesheet) STYLESHEET="$2" ; shift 2 ;;
        --suffix) SUFFIX="$2" ; shift 2 ;;
        --rst-options) RST_OPTS="$2"; shift 2 ;;
        -c|--clean) CLEAN=true; shift;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

if [ $# -ne 1 ] ; then
    REPO=$(pwd)
    echo "No directory argument, building RST files in $REPO"
else
    REPO=$(readlink -f $1)
    echo "Building RST files in '$REPO'"
fi

FILE_LIST=$(find $REPO -iname "*.$SUFFIX")
RST_OPTS="${RST_OPTS} --stylesheet ${STYLESHEET}"
MD5SUM=/usr/bin/md5sum
BUILT=""

html_suffix () {
    echo $1 | sed "s|\.$SUFFIX$|.html|"
}

md5_suffix () {
    echo $1 | sed "s|\.$SUFFIX$|.md5|"
}

checksum () {
    local sum=$(md5_suffix $1)
    ${MD5SUM} $1 > $sum
}

build_page () {
    local sum=$(md5_suffix $1)
    if [ -f $sum ] ; then
        ${MD5SUM} --check $sum &> /dev/null
        if [ $? -eq  0 ] ; then
            return
        fi
    fi
    local dest=$(html_suffix $1)
    ${RST2HTML} ${RST_OPTS} $1 > $dest
    [ $? -eq 0 ] && checksum $1
    BUILT="$BUILT\n  $1"
}

if $CLEAN ; then
    echo "Cleaning MD5 and HTML files from \"$REPO\""
    find $REPO -iname "*md5" -or -iname "*html" | xargs rm
    echo "... cleaning complete."
    exit 0;
fi

for file in $FILE_LIST; do
    build_page $file
done
if [ "$BUILT" != "" ] ; then
    echo -e "Files Built:$BUILT"
else
    echo "All files up to date."
fi
