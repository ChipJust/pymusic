#!python3
r""" player_back.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/player_back.svg'),
        'Back',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.player_back = player_back.__get__(parent)
    a.triggered.connect(parent.player_back)
    return a


def player_back(self):
    print(f"player_back")
    # bugbug: seek to the start of the project time
