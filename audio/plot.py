#!/usr/bin/env python
# Copyright 2016 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""plot.py : library for plotting audio waveforms"""

from matplotlib import pyplot


def plot_waveform(wavedata, channels, start_frame, end_frame):
    """Plot the given waveform with 1 channel per subplot."""
    try:
        wavedata = wavedata.transpose()
        _, subplots = pyplot.subplots(1, channels)
        if channels == 1:
            subplots.plot(wavedata[start_frame:end_frame])
        else:
            for channel in range(channels):
                subplots[channel].plot(
                    wavedata[channel][start_frame:end_frame])
        pyplot.show()
    finally:
        pyplot.close()
