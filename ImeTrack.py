#!python3
r""" ImeTrack.py



"""
import typing
import PySide6

class ImeTrack(PySide6.QtCore.QObject):
    name_changed_signal = PySide6.QtCore.Signal(str)

    def __init__(self, name=None):
        super().__init__()
        self._name = name
        # maybe a list or dict of wav files
        # and some way to process that list to produce a signal at the project time
        self.wavs = dict()

    @PySide6.QtCore.Property(str, notify=name_changed_signal)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed_signal.emit(value)

    def add_wav(self, filename):
        self.wav[filename] = open(filename, 'rb')


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

        self.track_name = PySide6.QtWidgets.QLineEdit(track.name)
        self.track_name.editingFinished.connect(self.edit_track_name)
        layout.addWidget(self.track_name)

    def edit_track_name(self):
        # reflect the user's manual update of track_name to the track object
        self.track.name = self.track_name.text()

    def update_track_name(self, value):
        # reflect the track object's update to the track_name
        self.track_name.setText(value)

"""
    def __init__(self, *args): The constructor to initialize your custom list. It should accept an optional iterable to populate the list initially.
    def __len__(self): Returns the number of elements in the list.
    def __getitem__(self, index): Accesses the element at the given index.
    def __setitem__(self, index, value): Sets the element at the given index to value.
    def __delitem__(self, index): Deletes the element at the given index.
    def __iter__(self): Enables iteration over the list.
    def __contains__(self, item): Checks if the list contains the specified item.
    def __str__(self): Returns a string representation of the list.
    def __repr__(self): Returns a string representation suitable for debugging.

    def append(self, item): Adds an item to the end of the list.
    def extend(self, iterable): Appends elements from an iterable to the list.
    def insert(self, index, item): Inserts an item at the specified index.
    def remove(self, item): Removes the first occurrence of the specified item.
    def pop(self, index=-1): Removes and returns the element at the given index (defaults to the last).
    def index(self, item): Returns the index of the first occurrence of the specified item.
    def count(self, item): Returns the number of occurrences of the specified item.
    def reverse(self): Reverses the order of elements in the list (in-place).
    def sort(self, key=None, reverse=False): Sorts the list in-place (optional key and reverse arguments).
    def clear(self): Removes all items from the list.
"""


class ImeTrackCollection(PySide6.QtCore.QObject):
    tracks_changed_signal = PySide6.QtCore.Signal()

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

