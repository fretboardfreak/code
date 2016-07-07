#!/bin/bash -x

TARGET=$1
OPTS=$2

# load configuration
. ~/bin/transfer_config.sh

remote_target=$(dirname ${TARGET})
if [[ "$remote_target" == "." ]]; then
    remote_target=""
fi

rsync -aP ${OPTS} ${TARGET} sandc3@${IP}:${REMOTE_BASE}/${remote_target}
