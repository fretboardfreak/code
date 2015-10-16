#!/bin/bash

# Profile Bash Scripts
# This script is used to collate profiling information that would be written by
# the following code.  Wrap this around the bash code you wish to profile...
#
# exec 3>&2 2> >(tee /tmp/profile.$$.time |\
#                sed -u 's/^.*$/now/' |\
#                date -f - +%s.%N > /tmp/profile.$$.time)
# set -x
# ... the bash code you want to profile
# set +x
# exec 2>&3 3>&-

PID=$1

TIMES=/tmp/profile.${PID}.time
LOG=/tmp/profile.${PID}.log

paste <(
    while read time ;do
        [ -z "$last" ] && last=${time//.} && first=${time//.}
        crt=000000000$((${time//.}-10#0$last))
        ctot=000000000$((${time//.}-10#0$first))
        printf "%12.9f %12.9f\n" ${crt:0:${#crt}-9}.${crt:${#crt}-9} \
                                 ${ctot:0:${#ctot}-9}.${ctot:${#ctot}-9}
        last=${time//.}
      done < ${TIMES}
  ) ${LOG} > /tmp/profile.${PID}.results
