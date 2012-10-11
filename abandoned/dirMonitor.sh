#!/bin/sh

# dirMonitor.sh is a bash script that monitors a directory and triggers
# another command when it notices changes.  It is meant to be run periodically
# with something like cron.

FOLDER=/home/csand/tmp/syncTest/stuff/notes/
TIMEMARKER=timemarker
TEMPFILE=temp

#use & after the command otherwise you can get a race condition
CMD="echo \"build the notes\"" 

#create a tempfile containing filenames of changed files
find $FOLDER -cnewer $TIMEMARKER > $TEMPFILE

#get a count of the number of changed files, run $CMD if there is more than 0
if [ `cat $TEMPFILE  | wc -l` -ne 0 ]
    then $CMD
fi

#cleanup the tempfile and updated the timemarker filestamp
rm $TEMPFILE && touch $TIMEMARKER
