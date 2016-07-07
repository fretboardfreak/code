#!/bin/bash -x

TARGET=$1
OPTS=$2

# load configuration
. ~/bin/transfer_config.sh

mkdir -p $(dirname ${TARGET})
rsync -aP ${OPTS} sandc3@${IP}:${REMOTE_BASE}/${TARGET} $(dirname ${TARGET})
