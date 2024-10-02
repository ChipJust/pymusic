r""" ImeMixerView.py



"""
import PySide6

import ImeAudioPlayer
import ImeTrack


class ImeMixerView(PySide6.QtWidgets.QWidget):
    # The view we are doing now is the "Reaper" view, which is providing
    # the functionality that we get from the REAPER DAW published by Cockos
    # see: https://www.reaper.fm/
    # Since Reaper is TM we will call this the "mixer" view.
    def __init__(self, parent):
        if not parent:
            raise ValueError(f"{self.__class__.__name__} must have valid parent")
        if not hasattr(parent, 'tracks'):
            raise ValueError(f"The parent passed to {self.__class__.__name__} must have an tracks attribute")
        super().__init__(parent)
        self.parent = parent

        # This is the main layout for the mixer view, a vertical box.
        # There are three rows in this box: track area, player controls and mix area
        # passing self to the constructor does self.setLayout(layout) automatically
        layout = PySide6.QtWidgets.QVBoxLayout(self)

        # Track area
        self.track_area = PySide6.QtWidgets.QTableWidget()
        self.track_area.setColumnCount(2)
        self.track_area.setHorizontalHeaderLabels(["Track", "Contents"])
        #self.track_area.horizontalHeader().setVisible(False)
        #self.track_area.verticalHeader().setVisible(False)
        parent.tracks.tracks_changed_signal.connect(self.update_track_table)
        self.update_track_table()
        layout.addWidget(self.track_area)

        # Player controls
        player_row = PySide6.QtWidgets.QWidget()
        player_row_layout = PySide6.QtWidgets.QHBoxLayout(player_row)
        layout.addWidget(player_row)
        parent.player = ImeAudioPlayer.ImeAudioPlayer(self, attached_actions=parent.attached_actions)
        player_row_layout.addWidget(parent.player.widget)
        player_row_layout.addWidget(PySide6.QtWidgets.QLabel("QLabel after the player"))
        player_row_layout.addWidget(PySide6.QtWidgets.QLabel("QLabel at end of row"))
        player_row_layout.setContentsMargins(0, 0, 0, 0)

        # Mix area
        layout.addWidget(PySide6.QtWidgets.QLabel("ImeMixerView: mixer area"))

    def update_track_table(self):
        self.track_area.setRowCount(len(self.parent.tracks))
        for row, track in enumerate(self.parent.tracks):
            track_handle = ImeTrack.ImeTrackHandle(self.track_area, track)
            self.track_area.setCellWidget(row, 0, track_handle)
            # bugbug: implement the content view
            #contents_item = PySide6.QtWidgets.QTableWidgetItem(str(track.wavs))
            #self.track_area.setItem(row, 1, contents_item)
