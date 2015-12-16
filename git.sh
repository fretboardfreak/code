#!/bin/sh

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

# A bash library to help with git hosting, and usage.

publishRepository () {
    # Assumes CWD is the bare repository to publish
    git --bare update-server-info
    mv hooks/post-update.sample hooks/post-update
    chmod a+x hooks/post-update
}

# Topic Branch Management

# TOPCI_DIR is where the topic data is persisted.  Must end with trailing '/'
# TOPIC_DIR can be set here or in .bashrc as an environment variable.
#TOPIC_DIR='/local/sandc3/git/topicMgmt/'

getBranchName () {
    branchName=$(git symbolic-ref -q HEAD)
    branchName=${branchName##refs/heads/}
    branchName=${branchName:-HEAD}

}

addTopic () {
    getBranchName
    local newTopic=${TOPIC_DIR}${1}
    touch ${newTopic}
    echo ${branchName} > ${newTopic}
    git checkout -b ${1} ${branchName}
    updateTopic
}

updateTopic () {
    getBranchName
    local currentBranch=$branchName
    local topicFile="$TOPIC_DIR$currentBranch"
    if [[ -f $topicFile ]]; then
        git checkout `cat $topicFile` && updateTopic && git checkout $currentBranch && git pull --rebase . `cat $topicFile`
    else
        git pull
    fi
}

removeTopic () {
    getBranchName
    local topicFile="$TOPIC_DIR$branchName"
    git checkout `cat ${topicFile}`
    rm ${topicFile}
    git branch -d $branchName
}
