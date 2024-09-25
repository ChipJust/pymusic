#!python3
r""" player_record.py



"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/player_record.svg'),
        'Forward',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.player_record = player_record.__get__(parent)
    a.triggered.connect(parent.player_record)
    return a


def player_record(self):
    print(f"player_record")
