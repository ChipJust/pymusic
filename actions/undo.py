#!python3
r""" undo.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/undo.svg'),
        'undo',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.undo = undo.__get__(parent)
    a.triggered.connect(parent.undo)
    return a


def undo(self):
    print(f"undo")
    # bugbug: do undo
