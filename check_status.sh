#!/bin/bash

# Copyright 2015 Curtis Sand
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

STATUS_FILE='status.txt'

usage () {
    echo -e "$SCRIPT [-h|--help|-f|--file-presence|-c|--status-contents]\n"
    local msg="Validate the contents of the ${STATUS_FILE} file compared to"
    msg="${msg} the task files present on the filesystem."
    msg="${msg} The default behaviour is to execute all checks"
    msg="${msg} but can be overridden with one of the options."
    echo $msg|fmt
    echo "  Options:"
    echo "    -h|--help            : print this help message"
    echo "    -f|--file-presence   : Check that the sub-directories"
    echo "                           contain all task files."
    echo "    -c|--status-contents : Check that ${STATUS_FILE} contains"
    echo "                           references to all task files."
    exit 1;
}

ARGS=`getopt -o "h,f,c" -l "help,file-presence,status-contents" \
    -n "check_status.sh" -- "$@"`
if [ $? -ne 0 ]; then
    # bad arguments found
    exit 1;
fi
eval set -- "$ARGS"

# logic flags
FILE_PRESENCE=false
EXECUTE_BOTH=true

while true ; do
    case "$1" in
        -h|--help) usage ; shift ;;
        -f|--file-presence) FILE_PRESENCE=true; EXECUTE_BOTH=false; shift ;;
        -c|--status-contents) EXECUTE_BOTH=false; shift ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

RC=0

if ! $FILE_PRESENCE; then
    echo "Default Logic: checking that \"${STATUS_FILE}\" is complete..."
    IFS=$'\n'  # use newline delimiter instead of space
    task_dirs=$(find . -maxdepth 1 -type d|sed -e 's@./@@'|grep -v "\.")
    tasks=$(find $task_dirs -type f -not -iname ".*swp" | \
            sed -e 's@^./@@' -e 's@`<@@g' -e 's@>`_@@')
    missing=
    for task in ${tasks}; do
        grep ${task} ${STATUS_FILE} -q
        if [[ "$?" -eq "0" ]]; then
            echo -n " ."
        else
            missing="${missing}\"${task}\"...\tNO \"${STATUS_FILE}\" ENTRY"
            RC=1
        fi
    done
    echo -e "${missing}"
else
    echo "Reverse Logic: checking all files referenced in \"${STATUS_FILE}\" exist..."
    tasks=$(grep "^\`<" ${STATUS_FILE}|sed -e "s@\`<@@" -e "s@>\`_@@")
    missing=""
    for task in ${tasks}; do
        if [[ -f $task ]]; then
            echo -n " ."
        else
            missing="${missing}\n\"$task\"...\tFILE MISSING";
        fi;
    done
    echo -e "${missing}"
fi

if $EXECUTE_BOTH; then
    if ! $FILE_PRESENCE; then
        args="--file-presence"
    else
        args="--status-contents"
    fi
    $SCRIPT $args
fi
exit ${RC}
