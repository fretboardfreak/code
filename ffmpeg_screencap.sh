#!/bin/bash
# Copyright 2017 Curtis Sand
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

# FFMPEG Screen Capture
# Captures silent video to OGG Theora encoded "mkv" video files.

# Usage: ffmpeg_screencap.sh OUTPUT_FILENAME

ffmpeg -video_size 1920x1080 -framerate 30 -f x11grab -i :0.0+1920,0 $@
