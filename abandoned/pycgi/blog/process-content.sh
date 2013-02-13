#!/bin/sh

RAW_CONTENT=$1
CONTENT=$2

for x in `ls $RAW_CONTENT`; do
    ./rst.py $RAW_CONTENT$x > $CONTENT$x.rst;
    echo "Compiled $RAW_CONTENT$x to $CONTENT$x.rst"
done;
rename -vf 's/\.txt\.rst$/\.rst/' $CONTENT*
