#!/usr/bin/env python

import numpy
from scikits.audiolab import Format, Sndfile

fname = 'test.wav'

framerate = 48000
channels = 2
clip_length = 1  # seconds

# Constant ints in the data array produces no sound.
#
# data = numpy.ndarray((framerate, channels))
# data_constant = 0.123
# for frame in range(framerate) * clip_length:
#     data[frame, 0] = data_constant
#     data[frame, 1] = data_constant


# Gausian white noise
data = numpy.random.randn(framerate * clip_length, channels)

output_file = Sndfile(fname, 'w', Format('wav'), channels, framerate)
output_file.write_frames(data)
output_file.close()
