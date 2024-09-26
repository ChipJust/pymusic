r""" ImeMixerView.py



"""
import PySide6

import ImeAudioPlayer


class ImeMixerView(PySide6.QtWidgets.QWidget):
    # The view we are doing now is the "Reaper" view, which is providing
    # the functionality that we get from the REAPER DAW published by Cockos
    # see: https://www.reaper.fm/
    # Since Reaper is TM we will call this the "mixer" view.
    def __init__(self, parent):
        if not parent:
            raise ValueError(f"{self.__class__.__name__} must have valid parent")
        if not hasattr(parent, 'attached_actions'):
            raise ValueError(f"The parent passed to {self.__class__.__name__} must have an attached_actions attribute")
        super().__init__(parent)

        layout = PySide6.QtWidgets.QVBoxLayout(self) # passing self to the constructor does self.setLayout(layout) automatically
        layout.addWidget(PySide6.QtWidgets.QLabel("ImeMixerView: track area"))
        player_row = PySide6.QtWidgets.QWidget()
        player_row_layout = PySide6.QtWidgets.QHBoxLayout(player_row)
        layout.addWidget(player_row)
        layout.addWidget(PySide6.QtWidgets.QLabel("ImeMixerView: mixer area"))

        # Player controls
        parent.player = ImeAudioPlayer.ImeAudioPlayer(self, attached_actions=parent.attached_actions)
        player_row_layout.addWidget(parent.player.widget)
        player_row_layout.addWidget(PySide6.QtWidgets.QLabel("QLabel after the player"))
        player_row_layout.addWidget(PySide6.QtWidgets.QLabel("QLabel at end of row"))
        player_row_layout.setContentsMargins(0, 0, 0, 0)

