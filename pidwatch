#!/bin/bash

# Copyright 2011 Curtis Sand
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

# TODO: this should be rewritten in python with some more options
#       like polling interval, type of notification, etc.

function usage() {
    echo "pidwatch.sh [-h] <pid>"
    echo "    Monitor the given pid.  When the process dies"
    echo "    notify the user via a popup message."
    echo "      -h - print this help message"
    exit 0
}

pid=
function pidwatch() {
    if [[ -z ${pid} ]]; then
        usage
    fi
    while [ true ]
    do
        ps --pid ${pid} > /dev/null
        val=$?
        if [[ ${val} -eq 1 ]]; then
            zenity --info --text "PID ${pid} appears to have stopped running"
            exit $?
        else
            # don't be too aggressive with the polling
            sleep 10
        fi
    done
}

function runTest() {
    while [ true ]
    do
        echo "blah"
    done
}

if [[ $# -eq 1 ]]; then
    if [[ ${1} = "-h" ]]; then
        usage
    fi
    pid=${1}
    pidwatch
else
    usage
fi
