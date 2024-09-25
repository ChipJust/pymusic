#!python3
r""" file_open.py - file_open action module

This module publishes the file_open action.
The main window's constructor loads this module and calls the attach_action
function, passing the main window's object.
This module must instantiate the action and attach both the action and its
related callback to the main window object, parent.

"""
import pathlib
import PySide6.QtWidgets
import PySide6.QtGui

icon = PySide6.QtGui.QIcon('./assets/file_open.svg')

def attach_action(parent):
    a = PySide6.QtGui.QAction(
        icon,
        'Open File',
        parent)
    a.setShortcut('Ctrl+O')
    parent.file_open_dialog = file_open_dialog.__get__(parent)
    a.triggered.connect(parent.file_open_dialog)
    return a


def file_open_dialog(self):
    filename, ok = PySide6.QtWidgets.QFileDialog.getOpenFileName(
        self,
        "Select a File",
        str(self.default_dir),
        "Any File Type (*.*);;Python (*.py);;Json (*.json)"
    )
    print(f"{filename=}, {ok=}")
    path = pathlib.Path(filename)
    print(f"{path=}")

# bugbug: connect this file to a track, i.e. put it in the track
# To accomplish this we must first define a starting data structure for
# tracks and for a track.
# Then we must make some sort of list view of the current tracks such
# that the user may select one (as similar to QFileDialog look and feel
# as possible).
# This dialog must have a button for adding a new track, which pops up
# a form to populate information about the track, such that all data
# defined to be part of its structure exists, either defaulted or user
# provided.

