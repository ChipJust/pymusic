#!python3
r""" ImeTrack.py



"""
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
