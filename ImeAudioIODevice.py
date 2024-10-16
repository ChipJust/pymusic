#!python3
r""" ImeAudioIODevice.py

newrel: list of things to do in this class
    - create a buffer for the mix
    - sum the track data into the buffer
    - there are now different indexs and positions that need translation
        - self.pos()    the byte position of ImeAudioIODevice from
                        ImeAudioPlayer's point of view
        - track.getData uses the index into the ys numpy array
                        this is a frame index, and each frame is 4 bytes
                        because we convert all formats to 32 bit arrays
        - mix buffer    we need to decide the width, but this is going
                        to also be an array of frames, either 32 or 64 wide
                        also indexed by frame, not byte or time
      this class should handle all the fix-ups needed translate from pos to
      indexes and visa-versa

    Copyright (c) 2024 Chip Ueltschey All rights reserved.
"""
import PySide6




class ImeAudioIODevice(PySide6.QtCore.QIODevice):

    def __init__(self, tracks):
        super().__init__()
        self.tracks = tracks


    def readData(self, maxSize):
        print(f"{self.__class__.__name__}.readData({maxSize=})")
        current_pos = self.pos()
        data = self.tracks[0].getData(current_pos, current_pos + maxSize)
        self.seek(current_pos + len(data))  # Update position
        return data

    def seek(self, pos):
        print(f"{self.__class__.__name__}.seek({pos=})")
        return super().seek(pos)  # Call base class implementation

    def isSequential(self):
        print(f"{self.__class__.__name__}.isSequential()")
        # Return True if your device is sequential, False if random-access
        return False

    def bytesAvailable(self):
        print(f"{self.__class__.__name__}.bytesAvailable()")
        # bugbug: need to do this operation on the project's mix buffer and not
        #         on the tracks themselves, but that requires that we make the
        #         project mix buffer first...
        if not self.tracks:
            return 0
        return max(0, self.tracks[0].totalSize() - self.pos())
