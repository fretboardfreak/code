#!/bin/sh

# Script borrowed from: https://help.github.com/articles/changing-author-info/

# Fill in OLD_EMAIL, CORRECT_NAME and CORRECT_EMAIL and run the script to
# correct the entire history of the git repository found in the CWD.

git filter-branch --env-filter '
OLD_EMAIL=""
CORRECT_NAME=""
CORRECT_EMAIL=""

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
