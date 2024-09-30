#!python3
r""" track_add.py



"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/track_add.svg'),
        'track_add',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.track_add = track_add.__get__(parent)
    a.triggered.connect(parent.track_add)
    return a


def track_add(self):
    print(f"track_add")
    # bugbug: do track_add
