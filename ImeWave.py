#!python3
r""" ImeWave.py

    The ImeWave is the internal representation of wave data,
    suitable for DSP operations.

    newrel: not all wave files are openable using the wave module.
            We need to be able to open all wav formats, and we would like to
            also support making wav data from with mp3 or m4a and possibly
            other formats. In each case we want to convert to a NumPy array
            This traceback shows where the problem is in the wave module:
                Traceback (most recent call last):
                  File "D:\_code\pymusic\actions\file_open.py", line 39, in file_open_dialog
                    new_track.add_wav(filename)
                  File "D:\_code\pymusic\ImeTrack.py", line 45, in add_wav
                    with wave.open(filename, 'rb') as f:
                         ^^^^^^^^^^^^^^^^^^^^^^^^^
                  File "C:\Python312\Lib\wave.py", line 649, in open
                    return Wave_read(f)
                           ^^^^^^^^^^^^
                  File "C:\Python312\Lib\wave.py", line 286, in __init__
                    self.initfp(f)
                  File "C:\Python312\Lib\wave.py", line 266, in initfp
                    self._read_fmt_chunk(chunk)
                  File "C:\Python312\Lib\wave.py", line 383, in _read_fmt_chunk
                    raise Error('unknown format: %r' % (wFormatTag,))
                wave.Error: unknown format: 3
            We might want to implement the wave file parsing ourselves so we
            can cover these formats without needing to install other software
            or codecs.
                Integer PCM Data Chunk
                    8
                    16
                    24
                    32
                Floating Point PCM Data Chunk
                    32
                    64
            Note that Reaper does not seem to be following the specification
            when it generates some WAV formats. For example it left out the
            "fact" and it looks like it left out "Extension Size" which should
            have been present and set to zero for type 3, the FP PCM

    This object was based on the Wave class published in
        https://github.com/AllenDowney/ThinkDSP/blob/master/code/thinkdsp.py
        The origional license notice for thinkdsp.py:
            Copyright 2013 Allen B. Downey
            License: MIT License (https://opensource.org/licenses/MIT)

    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import copy
import wave

import numpy


class ImeWave:
    """Represents a discrete-time waveform."""

    def __init__(self, ys, ts=None, framerate=11025, nchannels=1, nframes=0, sampwidth=None):
        """Initializes the wave.

        ys: wave array
        ts: array of times
        framerate: samples per second
        """
        self.ys = numpy.asanyarray(ys)
        self.framerate = framerate

        if ts is None:
            self.ts = numpy.arange(len(ys)) / self.framerate
        else:
            self.ts = numpy.asanyarray(ts)

        self.nchannels = nchannels
        self.nframes = nframes # should be the same as len(ys)...should we assert that?
        self.sampwidth = sampwidth # in bits - can we get this from inspecting ys?

    @classmethod
    def from_file(cls, filename):
        # bugbug: this is slow for large files, and files are expected to be
        #         large, so we need to either use some multithreading here or
        #         defer this work. We could consider doing the file read later.

        with wave.open(filename, 'rb') as f:
            nchannels = f.getnchannels()
            nframes = f.getnframes()
            sampwidth = f.getsampwidth()
            framerate = f.getframerate()
            z_str = f.readframes(nframes)
        print(f"{nchannels=}, {nframes=}, {sampwidth=}, {framerate=}")

        dtype_map = {1: numpy.int8, 2: numpy.int16, 3: "special", 4: numpy.int32}
        if sampwidth not in dtype_map:
            raise ValueError(f"{sampwidth=} unknown")
        if sampwidth == 3:
            xs = numpy.fromstring(z_str, dtype=numpy.int8).astype(numpy.int32)
            ys = (xs[2::3] * 256 + xs[1::3]) * 256 + xs[0::3]
        else:
            ys = numpy.fromstring(z_str, dtype=dtype_map[sampwidth])

        # If stereo...
        # bugbug: maybe mix it down? Or allow stereo signals?
        #         for now we force nchannels to 1 in the constructor below.
        #         We could either provice the stereo data, which will require
        #         a review of all functions to handle stereo or we can mix it
        #         down to mono, in which case we could possibly drop the
        #         nchannels from this __init__
        if nchannels == 2:
            ys = ys[::2]

        w = cls(ys, framerate=framerate, nchannels=1, nframes=nframes, sampwidth=sampwidth)

        # bugbug: do we really want to automatically normalize?
        #         Remove this comment if the answer is yes.
        #         Remove the following line of code if the answer is no.
        w.normalize()

        return w

    def totalSize(self):
        print(f"ImeWave().totalSize() = {self.ys.nbytes}")
        return self.ys.nbytes

    def copy(self):
        """Makes a copy.

        Returns: new Wave
        """
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.ys)

    @property
    def start(self):
        return self.ts[0]

    @property
    def end(self):
        return self.ts[-1]

    @property
    def duration(self):
        """Duration (property).

        returns: float duration in seconds
        """
        return len(self.ys) / self.framerate

    def __add__(self, other):
        """Adds two waves elementwise.

        other: Wave

        returns: new Wave
        """
        if other == 0:
            return self

        assert self.framerate == other.framerate

        # make an array of times that covers both waves
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        n = int(round((end - start) * self.framerate)) + 1
        ys = numpy.zeros(n)
        ts = start + numpy.arange(n) / self.framerate

        def add_ys(wave):
            i = find_index(wave.start, ts)

            # make sure the arrays line up reasonably well
            diff = ts[i] - wave.start
            dt = 1 / wave.framerate
            if (diff / dt) > 0.1:
                warnings.warn(
                    "Can't add these waveforms; their " "time arrays don't line up."
                )

            j = i + len(wave)
            ys[i:j] += wave.ys

        add_ys(self)
        add_ys(other)

        return Wave(ys, ts, self.framerate)

    __radd__ = __add__

    def __or__(self, other):
        """Concatenates two waves.

        other: Wave

        returns: new Wave
        """
        if self.framerate != other.framerate:
            raise ValueError("Wave.__or__: framerates do not agree")

        ys = numpy.concatenate((self.ys, other.ys))
        # ts = numpy.arange(len(ys)) / self.framerate
        return Wave(ys, framerate=self.framerate)

    def __mul__(self, other):
        """Multiplies two waves elementwise.

        Note: this operation ignores the timestamps; the result
        has the timestamps of self.

        other: Wave

        returns: new Wave
        """
        # the spectrums have to have the same framerate and duration
        assert self.framerate == other.framerate
        assert len(self) == len(other)

        ys = self.ys * other.ys
        return Wave(ys, self.ts, self.framerate)

    def max_diff(self, other):
        """Computes the maximum absolute difference between waves.

        other: Wave

        returns: float
        """
        assert self.framerate == other.framerate
        assert len(self) == len(other)

        ys = self.ys - other.ys
        return numpy.max(numpy.abs(ys))

    def convolve(self, other):
        """Convolves two waves.

        Note: this operation ignores the timestamps; the result
        has the timestamps of self.

        other: Wave or NumPy array

        returns: Wave
        """
        if isinstance(other, Wave):
            assert self.framerate == other.framerate
            window = other.ys
        else:
            window = other

        ys = numpy.convolve(self.ys, window, mode="full")
        # ts = numpy.arange(len(ys)) / self.framerate
        return Wave(ys, framerate=self.framerate)

    def diff(self):
        """Computes the difference between successive elements.

        returns: new Wave
        """
        ys = numpy.diff(self.ys)
        ts = self.ts[1:].copy()
        return Wave(ys, ts, self.framerate)

    def cumsum(self):
        """Computes the cumulative sum of the elements.

        returns: new Wave
        """
        ys = numpy.cumsum(self.ys)
        ts = self.ts.copy()
        return Wave(ys, ts, self.framerate)

    def quantize(self, bound, dtype):
        """Maps the waveform to quanta.

        bound: maximum amplitude
        dtype: numpy data type or string

        returns: quantized signal
        """
        return quantize(self.ys, bound, dtype)

    def apodize(self, denom=20, duration=0.1):
        """Tapers the amplitude at the beginning and end of the signal.

        Tapers either the given duration of time or the given
        fraction of the total duration, whichever is less.

        denom: float fraction of the segment to taper
        duration: float duration of the taper in seconds
        """
        self.ys = apodize(self.ys, self.framerate, denom, duration)

    def hamming(self):
        """Apply a Hamming window to the wave."""
        self.ys *= numpy.hamming(len(self.ys))

    def window(self, window):
        """Apply a window to the wave.

        window: sequence of multipliers, same length as self.ys
        """
        self.ys *= window

    def scale(self, factor):
        """Multplies the wave by a factor.

        factor: scale factor
        """
        self.ys *= factor

    def shift(self, shift):
        """Shifts the wave left or right in time.

        shift: float time shift
        """
        # TODO: track down other uses of this function and check them
        self.ts += shift

    def roll(self, roll):
        """Rolls this wave by the given number of locations."""
        self.ys = numpy.roll(self.ys, roll)

    def truncate(self, n):
        """Trims this wave to the given length.

        n: integer index
        """
        self.ys = truncate(self.ys, n)
        self.ts = truncate(self.ts, n)

    def zero_pad(self, n):
        """Trims this wave to the given length.

        n: integer index
        """
        self.ys = zero_pad(self.ys, n)
        self.ts = self.start + numpy.arange(n) / self.framerate

    def normalize(self, amp=1.0):
        """Normalizes the signal to the given amplitude.

        amp: float amplitude
        """
        high, low = abs(max(self.ys)), abs(min(self.ys))
        self.ys = amp * self.ys / max(high, low)

    def unbias(self):
        """Unbiases the signal."""
        self.ys = unbias(self.ys)

    def find_index(self, t):
        """Find the index corresponding to a given time."""
        n = len(self)
        start = self.start
        end = self.end
        i = round((n - 1) * (t - start) / (end - start))
        return int(i)

    def segment(self, start=None, duration=None):
        """Extracts a segment.

        start: float start time in seconds
        duration: float duration in seconds

        returns: Wave
        """
        if start is None:
            start = self.ts[0]
            i = 0
        else:
            i = self.find_index(start)

        j = None if duration is None else self.find_index(start + duration)
        return self.slice(i, j)

    def slice(self, i, j):
        """Makes a slice from a Wave.

        i: first slice index
        j: second slice index
        """
        ys = self.ys[i:j].copy()
        ts = self.ts[i:j].copy()
        return Wave(ys, ts, self.framerate)




