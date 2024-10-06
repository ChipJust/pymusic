#!python3
r""" file_open.py - file_open action module

This module publishes the file_open action.
The main window's constructor loads this module and calls the attach_action
function, passing the main window's object.
This module must instantiate the action and attach both the action and its
related callback to the main window object, parent.

    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""

import PySide6

import ImeTrack


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/file_open.svg'),
        'Open File',
        parent)
    a.setShortcut(PySide6.QtGui.QKeySequence(PySide6.QtCore.Qt.CTRL | PySide6.QtCore.Qt.Key_O))
    parent.file_open_dialog = file_open_dialog.__get__(parent)
    a.triggered.connect(parent.file_open_dialog)
    return a


def file_open_dialog(self):
    filename, ok = PySide6.QtWidgets.QFileDialog.getOpenFileName(
        self,
        "Select a File",
        str(self.default_dir),
        "Wave File (*.wav)"
    )
    print(f"{filename=}, {ok=}")
    if filename:
        new_track = ImeTrack.ImeTrack(filename)
        new_track.add_wav(filename)
        self.tracks.append(new_track)
    print(f"added to {self.tracks=}")

