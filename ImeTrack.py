#!python3
r""" ImeTrack.py

    ImeTrack bridges the DSP focused ImeWave to the QT toolchain.
    A ImeTrack is a project level container for one audio data stream.

    bugbug: move each class to its own module

    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import typing
import wave

import numpy

import PySide6
import PySide6.QtWidgets

import ImeWave

class ImeTrack(PySide6.QtCore.QObject):
    name_changed_signal = PySide6.QtCore.Signal(str)

    def __init__(self, name=None):
        super().__init__()
        self._name = name
        # maybe a list or dict of wav files
        # and some way to process that list to produce a signal at the project time
        self.ws = dict()
        # bugbug: connect these to the ImeTrackHandle and ImeTrackMixer
        self.mute = False
        self.solo = False
        self.volume = 1.0
        self.pan = 0

    @PySide6.QtCore.Property(str, notify=name_changed_signal)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed_signal.emit(value)

    def add_wav(self, filename):
        self.ws[filename] = ImeWave.ImeWave.from_file(filename)

    def getData(self, start, end):
        # bugbug: what we should be doing is looking up the start and end
        # frames in an as yet non-existing mapping from project time to wave
        # data to see which of the ImeWave objects and which location in that
        # object we should return data from
        w = next(iter(self.ws.values()))
        return w.ys[start:end]

    def totalSize(self):
        # bugbug: update when implementing map of project time to wav data
        print(f"ImeTrack({self.name}).totalSize()")
        w = next(iter(self.ws.values()))
        return w.totalSize()



    # bugbug: add method for extracting the series data
    #         Eventually we will need some sort of control structure
    #         that maps from the ws dict to project time,
    #         but as a first step, assume one file and provide its data.


class ImeTrackHandle(PySide6.QtWidgets.QWidget):
    def __init__(self, parent, track):
        if not parent:
            raise ValueError(f"{self.__class__.__name__} must have valid {parent=}")
        if not track:
            raise ValueError(f"{self.__class__.__name__} must have valid {track=}")
        if not isinstance(track, ImeTrack):
            raise ValueError(f"{self.__class__.__name__} {track=} must be an instance of ImeTrack")
        super().__init__(parent)
        self.track = track
        self.track.name_changed_signal.connect(self.update_track_name)

        layout = PySide6.QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # newrel: add missing elements to this control and improve its look
        #         record arm button, mute, solo

        self.track_name = PySide6.QtWidgets.QLineEdit(track.name)
        self.track_name.editingFinished.connect(self.edit_track_name)
        layout.addWidget(self.track_name)

    def edit_track_name(self):
        # reflect the user's manual update of track_name to the track object
        self.track.name = self.track_name.text()

    def update_track_name(self, value):
        # reflect the track object's update to the track_name
        self.track_name.setText(value)


# newrel: add class for track content widget
#         update ImeMixerView.update_track_table to instantiate this class and
#         add it to the table
class ImeTrackMixer(PySide6.QtWidgets.QWidget):
    def __init__(self, parent, track):
        super().__init__(parent)


class ImeTrackCollection(PySide6.QtCore.QObject):
    tracks_changed_signal = PySide6.QtCore.Signal()

    # This is a list-like container that emits a signal when the list changes.

    def __init__(self, initial_tracks: typing.Iterable[typing.Any] = ()):
        super().__init__()
        self._tracks: typing.List[typing.Any] = list(initial_tracks)

    def __len__(self) -> int:
        """Returns the number of elements in the list."""
        return len(self._tracks)

    def __getitem__(self, index: int) -> typing.Any:
        """Accesses the element at the given index."""
        return self._tracks[index]

    def __setitem__(self, index: int, value: typing.Any):
        """Sets the element at the given index to value."""
        self._tracks[index] = value
        self.tracks_changed_signal.emit()

    def __delitem__(self, index: int):
        """Deletes the element at the given index."""
        del self._tracks[index]
        self.tracks_changed_signal.emit()

    def __iter__(self):
        """Enables iteration over the list."""
        return iter(self._tracks)

    def __contains__(self, item: typing.Any) -> bool:
        """Checks if the list contains the specified item."""
        return item in self._tracks

    def __str__(self) -> str:
        """Returns a string representation of the list."""
        return str(self._tracks)

    def __repr__(self) -> str:
        """Returns a string representation suitable for debugging."""
        return f"ImeTrackCollection({self._tracks})"

    def append(self, item: typing.Any):
        """Adds an item to the end of the list."""
        self._tracks.append(item)
        self.tracks_changed_signal.emit()

    def extend(self, iterable: typing.Iterable[typing.Any]):
        """Appends elements from an iterable to the list."""
        self._tracks.extend(iterable)
        self.tracks_changed_signal.emit()

    def insert(self, index: int, item: typing.Any):
        """Inserts an item at the specified index."""
        self._tracks.insert(index, item)
        self.tracks_changed_signal.emit()

    def remove(self, item: typing.Any):
        """Removes the first occurrence of the specified item."""
        self._tracks.remove(item)
        self.tracks_changed_signal.emit()

    def pop(self, index: int = -1) -> typing.Any:
        """Removes and returns the element at the given index (defaults to the last)."""
        item = self._tracks.pop(index)
        self.tracks_changed_signal.emit()
        return item

    def index(self, item: typing.Any) -> int:
        """Returns the index of the first occurrence of the specified item."""
        return self._tracks.index(item)

    def count(self, item: typing.Any) -> int:
        """Returns the number of occurrences of the specified item."""
        return self._tracks.count(item)

    def reverse(self):
        """Reverses the order of elements in the list (in-place)."""
        self._tracks.reverse()
        self.tracks_changed_signal.emit()

    def sort(self, key: typing.Optional[typing.Callable] = None, reverse: bool = False):
        """Sorts the list in-place (optional key and reverse arguments)."""
        self._tracks.sort(key=key, reverse=reverse)
        self.tracks_changed_signal.emit()

    def clear(self):
        """Removes all items from the list."""
        self._tracks.clear()
        self.tracks_changed_signal.emit()

