#!python3
r""" open_file.py - open_file action module

This module publishes the open_file action.
The main window's constructor loads this module and calls the attach_action
function, passing the main window's object.
This module must instantiate the action and attach both the action and its
related callback to the main window object, parent.

"""
import pathlib
import PySide6.QtWidgets
import PySide6.QtGui


def attach_action(parent):
    open_action = PySide6.QtGui.QAction(PySide6.QtGui.QIcon('./assets/arrow-down-from-arc2.svg'), 'Open File', parent)
    open_action.setShortcut('Ctrl+O')
    parent.open_file_dialog = open_file_dialog.__get__(parent)
    open_action.triggered.connect(parent.open_file_dialog)
    return open_action


def open_file_dialog(self):
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

