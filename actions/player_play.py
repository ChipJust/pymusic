#!python3
r""" player_play.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/player_play.svg'),
        'Play',
        parent)
    a.setShortcut(PySide6.QtGui.QKeySequence(PySide6.QtCore.Qt.CTRL | PySide6.QtCore.Qt.Key_P))
    parent.player_play = player_play.__get__(parent)
    a.triggered.connect(parent.player_play)
    return a


def player_play(self):
    print(f"player_play")
    self.player.play()
