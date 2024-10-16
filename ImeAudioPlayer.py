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


class ImeAudioPlayer(PySide6.QtCore.QObject):
    def __init__(self, parent, attached_actions):
        super().__init__(parent)

        # newrel: setup the signals to make this a project setting, such that
        #         if the user changes it we will reinit our player with the new
        #         device
        self.audio_device = PySide6.QtMultimedia.QMediaDevices.defaultAudioOutput()

        # Create a QAudioFormat object and set its properties
        # newrel: make the audio format configurable at the project level.
        self.audio_format = PySide6.QtMultimedia.QAudioFormat()
        # bugbug: these settings are all questionable...and may need to be
        #         configurable
        self.audio_format.setSampleRate(44100)
        self.audio_format.setChannelCount(1)
        #self.audio_format.setSampleFormat(PySide6.QtMultimedia.QAudioFormat.Int32)
        self.audio_format.setSampleFormat(PySide6.QtMultimedia.QAudioFormat.Int16)


        # newrel: if either the device or the format change at the project
        #         level we need to create a new sink using the new device and
        #         format
        self.audio_sink = PySide6.QtMultimedia.QAudioSink(self.audio_device, self.audio_format)
        self.audio_sink.stateChanged.connect(self.on_state_changed)


        # bugbug: connnect this to an interface signal
        self.set_volume(1.0)

        self.io_device = ImeAudioIODevice.ImeAudioIODevice(parent.parent.tracks)
        self.io_device.open(PySide6.QtCore.QIODevice.ReadOnly)
        print(f"{self.io_device.isSequential()=}, {self.io_device.pos()=}")
        #self.setSourceDevice(self.io_device)
        self.audio_sink.start(self.io_device)

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

    def play(self):
        print(f"play")
        if self.audio_sink.state() == PySide6.QtMultimedia.QAudio.State.StoppedState:
            self.audio_sink.start(self.io_device)
        elif self.audio_sink.state() == PySide6.QtMultimedia.QAudio.State.SuspendedState:
            self.audio_sink.resume()

    def pause(self):
        print(f"pause")
        if self.audio_sink.state() == PySide6.QtMultimedia.QAudio.State.ActiveState:
            self.audio_sink.suspend()
        elif self.audio_sink.state() == PySide6.QtMultimedia.QAudio.State.SuspendedState:
            self.audio_sink.resume()

    def stop(self):
        print(f"stop")
        if self.audio_sink.state() != PySide6.QtMultimedia.QAudio.State.StoppedState:
            self.audio_sink.stop()
            self.io_device.reset()  # Reset the IO device to the beginning

    @PySide6.QtCore.Slot(PySide6.QtMultimedia.QAudio.State)
    def on_state_changed(self, state):
        print(f"on_state_changed({state=})")
        if state == PySide6.QtMultimedia.QAudio.State.IdleState:
            # This is emitted when the audio device has no more data to process
            self.stop()

    def set_volume(self, volume):
        print(f"set_volume({volume=})")
        # volume should be between 0.0 and 1.0
        self.audio_sink.setVolume(volume)
