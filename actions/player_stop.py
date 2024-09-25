#!python3
r""" player_stop.py



"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/player_stop.svg'),
        'Forward',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.player_stop = player_stop.__get__(parent)
    a.triggered.connect(parent.player_stop)
    return a


def player_stop(self):
    print(f"player_stop")
    self.player.stop()
