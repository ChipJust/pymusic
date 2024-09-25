#!python3
r""" player_forward.py



"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/player_forward.svg'),
        'Forward',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.player_forward = player_forward.__get__(parent)
    a.triggered.connect(parent.player_forward)
    return a


def player_forward(self):
    print(f"player_forward")
