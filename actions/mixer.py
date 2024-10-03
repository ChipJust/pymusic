#!python3
r""" mixer.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/mixer.svg'),
        'mixer',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.mixer = mixer.__get__(parent)
    a.triggered.connect(parent.mixer)
    return a


def mixer(self):
    print(f"mixer")
    # bugbug: do mixer
