#!python3
r""" ImeAudioPlayer.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6
import PySide6.QtMultimedia

import ImeAudioIODevice


player_buttons = [
    'player_back',
    'player_forward',
    'player_record',
    'player_play',
    'player_stop',
    'player_pause',
]


class ImeAudioPlayer(PySide6.QtMultimedia.QMediaPlayer):
    def __init__(self, parent, attached_actions, audio_output=None):
        super().__init__(parent)

        # If audio_output is provided then the parent is already managing this detail
        # If audio_output is not provided create the default one and attach it to the parent object
        if not audio_output:
            audio_output = PySide6.QtMultimedia.QAudioOutput()
        self.audio_output = audio_output
        self.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)  # Set volume with float in range 0.0 to 1.0

        self.setSource("D:/Reaper/Rock of Ages/Rock of Ages.wav")  # bugbug: connect this to whatever the final is or mix to or something...

        self.io_device = ImeAudioIODevice.ImeAudioIODevice(self.audio_output)
        #self.io_device.open(QtCore.QIODevice.ReadOnly)
        #self.setSourceDevice(self.io_device)

        self.widget = PySide6.QtWidgets.QWidget()
        self.widget.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Fixed, PySide6.QtWidgets.QSizePolicy.Fixed)
        layout = PySide6.QtWidgets.QHBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for action_name in player_buttons:
            if action_name not in attached_actions:
                print(f"Player button is missing '{action_name}'")
                continue
            button = PySide6.QtWidgets.QPushButton()
            button.setIcon(attached_actions[action_name].icon())
            button.clicked.connect(attached_actions[action_name].trigger)
            button.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Fixed, PySide6.QtWidgets.QSizePolicy.Fixed)
            layout.addWidget(button, alignment=PySide6.QtCore.Qt.AlignLeft)
