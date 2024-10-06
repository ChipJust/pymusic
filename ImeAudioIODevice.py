#!python3
r""" ImeAudioIODevice.py



    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6




class ImeAudioIODevice(PySide6.QtCore.QIODevice):
    def __init__(self, audio_output):
        super().__init__()

    # This is the one that needs to provide the agregated data to the player at the requested project time
    # To do this we need all the sources of data, i.e. the tracks
    # We may need to have access to project time, but it seems better to provide that as an input to the funtion
    # We need to know the project's frame rate
