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

DIR="./"

usage () {
    echo "$SCRIPT [-h|--help] [OPTIONS] PID";
    echo -e "\nProfile Bash Scripts\n--------------------"
    echo "This script is used to collate profiling information that would be"
    echo "written by the following bash code.  Wrap this around the bash code"
    echo "you wish to profile..."
    echo ""
    echo "exec 3>&2 2> >(tee /tmp/profile.\$\$.log |\""
    echo "               sed -u 's/^.*$/now/' |\""
    echo "               date -f - +%s.%N > /tmp/profile.\$\$.time)"
    echo "set -x"
    echo "... the bash code you want to profile"
    echo "set +x"
    echo "exec 2>&3 3>&-"
    echo ""
    echo "  Options:"
    echo "    -h|--help     Show this help message."
    echo "    -d|--dir DIR  Directory containing the *.time and *.log files."
    echo ""
    echo "Note: this code was borrowed from one of the answers to this stack overflow"
    echo "topic:"
    echo "http://stackoverflow.com/questions/5014823/how-to-profile-a-bash-shell-script"

    exit 1;
}

ARGS=`getopt -o "hd:" -l "help,dir:" -n "profile_bash.sh" -- "$@"`
if [ $? -ne 0 ]; then
    # bad arguments found
    exit 1;
fi
eval set -- "$ARGS"

while true ; do
    case "$1" in
        -h|--help) usage ; shift ;;
        -d|--dir) DIR=$2 ; shift 2 ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

PID=$1

case "$DIR" in  # ensure trailing slash in path
    */) ;; # noop
    *) $DIR="${DIR}/"
esac

base=${DIR}*.${PID}
TIMES=$(readlink -f ${base}.time)
LOG=$(readlink -f ${base}.log)
RESULT=$(echo $LOG | sed 's/log$/results/g')
base=  # unset temp var

# check that TIMES and LOG files exist
if [ ! -f ${TIMES} ] ; then
    echo "Cannot find timestamp file at path '${TIMES}'"
    usage
    exit 1
fi
if [ ! -f ${LOG} ] ; then
    echo "Cannot find log file at path '${LOG}'"
    usage
    exit 1
fi

# check that RESULT file does not exist
if [ -f ${RESULT} ] ; then
    echo "Result file already exists, '${RESULT}'. Cannot proceed."
    exit 1;
fi

paste <(
    while read time ;do
        [ -z "$last" ] && last=${time//.} && first=${time//.}
        crt=000000000$((${time//.}-10#0$last))
        ctot=000000000$((${time//.}-10#0$first))
        printf "%12.9f %12.9f\n" ${crt:0:${#crt}-9}.${crt:${#crt}-9} \
                                 ${ctot:0:${#ctot}-9}.${ctot:${#ctot}-9}
        last=${time//.}
    done < ${TIMES}
) ${LOG} > ${RESULT}

echo "Results have been written to '${RESULT}'."
