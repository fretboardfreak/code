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

# Sine Wave Generation
# Data Normalized between -1 and 1
# Sinusoid Wave Amplitude = math.sin(frame/((framerate/frequency)/math.pi))
frequency = 440.0  # Hz (Concert Pitch A4)
framecount = framerate * clip_length
wavedata = numpy.ndarray((framecount, channels))
for frame in range(framecount):
    # Left track is 1 constant frequency
    wavedata[frame, 0] = math.sin(frame/((framerate/frequency)/math.pi))

    # Right track linearly progresses from 1 octave below to 1 octave above the
    # chosen frequency
    start_freq = frequency / 2
    end_freq = frequency * 2
    current_freq = start_freq + frame * (end_freq/framecount)
    wavedata[frame, 1] = math.sin(frame/((framerate/current_freq)/math.pi))

output_file = Sndfile(fname, 'w', Format('wav'), channels, framerate)
output_file.write_frames(wavedata)
output_file.close()
