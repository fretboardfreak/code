#!/usr/bin/env python
"""A Waveform or Signal Generator Library for creating audio waveforms."""

import sys
import argparse
import math

import numpy

VERSION = "0.1"


class Generator(object):
    def __init__(self, length=1.0, framerate=44100, verbose=False):
        self.length = length
        self.framerate = framerate
        self.verbose = verbose

    def _init(self, length=None, framerate=None, verbose=None, **kwargs):
        if length:
            self.length = length
        if framerate:
            self.framerate = framerate
        if verbose:
            self.verbose = verbose

        # framecount = frames/sec * sec
        self.framecount = int(self.framerate * self.length)
        # rectify length to actual framecount
        self.length = float(self.framecount)/self.framerate
        self.dprint('framecount = %s' % self.framecount)
        self.dprint('rectified length = %s' % self.length)
        self.wavedata = numpy.zeros((self.framecount, 1))

    def dprint(self, msg):
        """Conditionally print a debugging message."""
        if self.verbose:
            print(msg)

    def whitenoise(self, *args, **kwargs):
        """Random Gaussian White Noise."""
        self._init(*args, **kwargs)
        self.wavedata = numpy.random.randn(self.framecount, 1)
        return self.wavedata

    def _sinusoid_amplitude(self, frame, frequency):
        """Calculate the amplitude of a sinusoid wave at a given frequency."""
        # avoid divide by zero
        frame = 0.001 if frame is 0 else frame
        return math.sin(frame /
                        ((self.framerate / frequency) / math.pi))

    def sin_constant(self, frequency, *args, **kwargs):
        """Sinusoid wave of constant frequency."""
        self._init(*args, **kwargs)
        frequency = float(frequency)
        for frame in range(self.framecount):
            amplitude = self._sinusoid_amplitude(frame, frequency)
            self.wavedata[frame, 0] = amplitude
        return self.wavedata

    def sin_linear(self, start_freq, end_freq, *args, **kwargs):
        """Sinusoid wave of linearly changing frequency."""
        self._init(*args, **kwargs)
        for frame in range(self.framecount):
            # freq = start_freq + frame * freq_rate
            # freq_rate = total_freq_change / framecount
            frequency = start_freq + frame * (
                float(end_freq - start_freq) / self.framecount)
            amplitude = self._sinusoid_amplitude(frame, frequency)
            self.wavedata[frame, 0] = amplitude
        return self.wavedata


if __name__ == '__main__':
    DOC="""A Demonstration Program for the Signal Generator."""
    import wav_file
    import plot

    VERBOSE = False
    DEBUG = False

    def whitenoise(args, generator):
        generator.whitenoise()


    def sin_constant(args, generator):
        generator.sin_constant(args.frequency)


    def sin_linear(args, generator):
        generator.sin_linear(args.frequency/2, args.frequency*2)


    UI_MAP = {'noise': whitenoise, 'constant': sin_constant,
              'linear': sin_linear}


    def main():
        args = parse_cmd_line()

        sg = Generator(length=args.length, verbose=args.debug)

        UI_MAP[args.type](args, sg)

        if args.plot:
            plot.plot_waveform(sg.wavedata, 1, 0, sg.framecount)
        else:
            wfile = wav_file.WavFile(args.filename, 1, sg.framecount)
            try:
                wfile.write(sg.wavedata)
            finally:
                wfile.close()

        return 0


    def parse_cmd_line():
        parser = argparse.ArgumentParser(description=DOC)
        parser.add_argument(
            '--version', help='Print the version and exit.', action='version',
            version='%(prog)s {}'.format(VERSION))
        DebugAction.add_parser_argument(parser)
        VerboseAction.add_parser_argument(parser)

        parser.add_argument(
            '--filename',
            help='File to write the generated waveform to.')
        parser.add_argument(
            '-l', '--length', type=float,
            help='Length in seconds of the generated wav.')
        parser.add_argument(
            '-p', '--plot', help='Plot the waveform instead. '
            'Warning: Use a small length (e.g. 0.05) or the plot '
            'will be massive.', action='store_true')
        parser.add_argument(
            '-t', '--type', help='Type of signal to generate',
            choices=UI_MAP.keys())
        parser.add_argument(
            '-f', '--frequency', help='Frequency to use.', type=float)

        parser.set_defaults(filename='signal.wav', length=1.0, debug=False,
                            frequency=480, type='constant')
        return parser.parse_args()


    def dprint(msg):
        """Conditionally print a debug message."""
        if DEBUG:
            print(msg)


    def vprint(msg):
        """Conditionally print a verbose message."""
        if VERBOSE:
            print(msg)


    class DebugAction(argparse.Action):
        """Enable the debugging output mechanism."""

        flag = '--debug'
        help = 'Enable debugging output.'

        @classmethod
        def add_parser_argument(cls, parser):
            parser.add_argument(cls.flag, help=cls.help, action=cls)

        def __init__(self, option_strings, dest, **kwargs):
            super(DebugAction, self).__init__(option_strings, dest, nargs=0,
                                              default=False, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            print('Enabling debugging output.')
            global DEBUG
            DEBUG = True
            setattr(namespace, self.dest, True)


    class VerboseAction(DebugAction):
        """Enable the verbose output mechanism."""

        flag = '--verbose'
        help = 'Enable verbose output.'

        def __call__(self, parser, namespace, values, option_string=None):
            print('Enabling verbose output.')
            global VERBOSE
            VERBOSE = True
            setattr(namespace, self.dest, True)


    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if DEBUG:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
