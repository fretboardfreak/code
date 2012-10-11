#!/bin/sh

#Syncs a non-git directory with a directory managed by git

## Non git related stuff
$NONGITDIR=
$COMMITMSG=

## git config
### path to .git dir (e.g. /home/csand/stuff/.git)
$GITDIR=
### path to top level of working directory (e.g. /home/csand/stuff/)
$WORKTREE=
### path to the directory to synchronize (e.g. /home/csand/stuff/notes/) 
$SYNCDIR=

#get new changes from non git dir
rsync -haP --no-whole-file --inplace -ru $NONGITDIR/* $SYNCDIR

git --git-dir=$GITDIR --work-tree=$WORKTREE add $SYNCDIR/*
git --git-dir=$GITDIR --work-tree=$WORKTREE commit -m $COMMITMSG

if [ $? -eq 0 ] 
    then git --git-dir=$GITDIR --work-tree=$WORKTREE pull --rebase && \
            git --git-dir=$GITDIR --work-tree=$WORKTREE push
else 
    git --git-dir=$GITDIR --work-tree=$WORKTREE pull
fi

#put git changes into dropbox
rsync -haP --no-whole-file --inplace -ru $SYNCDIR/* $NONGITDIR

