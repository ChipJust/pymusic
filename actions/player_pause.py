#!python3
r""" player_pause.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6.QtGui
import PySide6.QtMultimedia


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/player_pause.svg'),
        'Pause',
        parent)
    a.setShortcut(PySide6.QtCore.Qt.Key_Space)
    parent.player_pause = player_pause.__get__(parent)
    a.triggered.connect(parent.player_pause)
    return a


def player_pause(self):
    print(f"player_pause")
    self.player.pause()
