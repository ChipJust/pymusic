#!python3
r""" track_add.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/track_add.svg'),
        'track_add',
        parent)
    a.setShortcut(PySide6.QtGui.QKeySequence(PySide6.QtCore.Qt.CTRL | PySide6.QtCore.Qt.Key_T))
    parent.track_add = track_add.__get__(parent)
    a.triggered.connect(parent.track_add)
    return a


def track_add(self):
    print(f"track_add")
    # bugbug: do track_add
