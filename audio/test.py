#!/usr/bin/env python

import numpy
from scikits.audiolab import Format, Sndfile
import math

fname = 'test.wav'

framerate = 48000
channels = 2
clip_length = 1  # seconds

# Constant ints in the wavedata array produces no sound.
#
# wavedata = numpy.ndarray((framerate, channels))
# data_constant = 0.123
# for frame in range(framerate) * clip_length:
#     wavedata[frame, 0] = data_constant
#     wavedata[frame, 1] = data_constant

# Gausian white noise
#
# wavedata = numpy.random.randn(framerate * clip_length, channels)

# Sine Wave Normalized between amplitude -1 and 1
# The stereo tracks are duplicated to simulate mono
frequency = 480  # Hz
framecount = framerate * clip_length
wavedata = numpy.ndarray((framecount, channels))
for frame in range(framecount):
    value = math.sin(frame/((framerate/frequency)/math.pi))
    wavedata[frame, 0] = value
    wavedata[frame, 1] = value

output_file = Sndfile(fname, 'w', Format('wav'), channels, framerate)
output_file.write_frames(wavedata)
output_file.close()
