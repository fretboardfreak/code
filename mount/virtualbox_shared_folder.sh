#!/bin/bash
# Copyright 2016 Curtis Sand
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

MOUNT="/usr/sbin/mount.vboxsf"

# Shared folder name is the name given in the VirtualBox UI to the folder.
SHARED_FOLDER_NAME="C_DRIVE"
MOUNTPOINT="/home/sandc3/cdrive"
OPTIONS="-o uid=$(id -u),gid=$(id -g),rw "

sudo $MOUNT $OPTIONS $SHARED_FOLDER_NAME $MOUNTPOINT
