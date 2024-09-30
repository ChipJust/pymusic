#!python3
r""" redo.py



"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/redo.svg'),
        'redo',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.redo = redo.__get__(parent)
    a.triggered.connect(parent.redo)
    return a


def redo(self):
    print(f"redo")
    # bugbug: do redo
