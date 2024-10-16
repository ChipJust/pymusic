r""" ImeMixerView.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6

import ImeAudioPlayer
import ImeTrack

class ImeMixerView(PySide6.QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._validate_parent(parent)
        self.parent = parent

        layout = PySide6.QtWidgets.QVBoxLayout(self)

        self._setup_track_area(layout)
        self._setup_player_controls(layout)
        self._setup_mix_area(layout)

    def _validate_parent(self, parent):
        if not parent:
            raise ValueError(f"{self.__class__.__name__} must have a valid parent")
        if not hasattr(parent, 'tracks'):
            raise ValueError(f"The parent of {self.__class__.__name__} must have a 'tracks' attribute")

    def _setup_track_area(self, layout):
        # newrel: maybe this widget should be instantiated in the
        #         ImeTrackCollection class as the .widget attribute of that
        #         class self.track_area would be replaced with
        #         self.parent.tracks.widget and update_track_table could move
        #         to be a method of ImeTrackCollection
        self.track_area = PySide6.QtWidgets.QTableWidget()
        self.track_area.setColumnCount(2)
        self.track_area.setHorizontalHeaderLabels(["Track", "Contents"])
        self.parent.tracks.tracks_changed_signal.connect(self.update_track_table)
        self.update_track_table()
        layout.addWidget(self.track_area)

    def _setup_player_controls(self, layout):
        player_row = PySide6.QtWidgets.QWidget()
        player_row_layout = PySide6.QtWidgets.QHBoxLayout(player_row)
        self.parent.player = ImeAudioPlayer.ImeAudioPlayer(self, attached_actions=self.parent.attached_actions)
        player_row_layout.addWidget(self.parent.player.widget)
        player_row_layout.addWidget(PySide6.QtWidgets.QLabel("QLabel after the player"))
        player_row_layout.addWidget(PySide6.QtWidgets.QLabel("QLabel at end of row"))
        player_row_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(player_row)

    def _setup_mix_area(self, layout):
        # bugbug: implement mixing controls
        layout.addWidget(PySide6.QtWidgets.QLabel("ImeMixerView: mixer area"))

    def update_track_table(self):
        self.track_area.setRowCount(len(self.parent.tracks))
        for row, track in enumerate(self.parent.tracks):
            track_handle = ImeTrack.ImeTrackHandle(self.track_area, track)
            self.track_area.setCellWidget(row, 0, track_handle)
            # bugbug: implement the content view
            #contents_item = PySide6.QtWidgets.QTableWidgetItem(str(track.wavs))
            #self.track_area.setItem(row, 1, contents_item)
