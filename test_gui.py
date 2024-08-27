#!python3
r""" test_gui.py

Draw the equivalent charts as this notebook
http://localhost:8888/notebooks/librosa_demo.ipynb

Dependencies
    py -m pip install pyside6
    cd %YOUR_CODE_ROOT% && git clone https://github.com/adactio/TheSession-data

Source for pyside6: git clone https://code.qt.io/pyside/pyside-setup

"""
import argparse
import pathlib
import sys

# From notebook
import matplotlib.pyplot as plt

import seaborn
seaborn.set(style='ticks')

from IPython.display import Audio

import numpy as np
import scipy
import mir_eval
import librosa

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#import pandas as pd

import PySide6.QtCharts
import PySide6.QtCore
import PySide6.QtMultimedia
import PySide6.QtWidgets

class LibrosaDemo():
    pass


def parse():
    current_script_path = pathlib.Path(__file__).resolve()
    repo_root = current_script_path.parent.parent.parent
    code_root = repo_root.parent
    #print(f"{current_script_path=}, {repo_root=} {code_root=}")
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--session_db",
        type=pathlib.Path,
        default=code_root / "TheSession-data" / "thesession.db",
        help="Filepath for a file containing the SQL commands that initialize the database")
    args, remaining = parser.parse_known_args()

    return args, remaining


def work():
    y, sr = librosa.load(librosa.example('vibeace', hq=True))
    Audio(data=y, rate=sr)
    # what does this return and how do I put that as a widget in the app.
    librosa.display.waveshow(y, sr=sr)
    # how do I put that on the canvas

    # Display Power
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, y_axis='linear', x_axis='time')
    plt.colorbar()
    # need to put this picture on there somwhere
    # would be super-sweet if we could line this one's time axis (x_axis) with the previous one, and all of them really
    # i.e. they should all be of same width on the display, and if we need to be able to scroll to the left or right they all scroll together aligned

    # Display Log Power
    librosa.display.specshow(D, y_axis='log', x_axis='time')
    plt.colorbar()

    # Constant Q Transform
    cqt_power = librosa.amplitude_to_db(np.abs(librosa.cqt(y, sr=sr)), ref=np.max)
    librosa.display.specshow(cqt_power, y_axis='cqt_hz', x_axis='time')
    plt.colorbar()

    # there should be some sort of class that is managing all this app to gui binding

    # Let's call it file view: or perhapse view: file
    # Show a standard (or configurable) set of content
    # In our example we need to show:
    #    Audio() player: show that graphic and make its controls work so we can listen to the file
    #    librosa.display.waveshow(y, sr=sr)
    #    Display Power
    #    Display Log Power
    #    Constant Q Transform
    #    librosa.feature.melspectrogram
    #    librosa.feature.chroma_cqt
    #    librosa.feature.tonnetz


class MainWindow(PySide6.QtWidgets.QMainWindow):
    def __init__(self, device, sr=None, sample_count=2000, resolution=4):
        super().__init__()
        self.sr = sr if sr else device.maximumSampleRate()
        self.sample_count = sample_count
        self.resolution = resolution

        self._series = PySide6.QtCharts.QLineSeries()
        self._chart = PySide6.QtCharts.QChart()
        self._chart.addSeries(self._series)
        self._axis_x = PySide6.QtCharts.QValueAxis()
        self._axis_x.setRange(0, self.sample_count)
        self._axis_x.setLabelFormat("%g")
        self._axis_x.setTitleText("Samples")
        self._axis_y = PySide6.QtCharts.QValueAxis()
        self._axis_y.setRange(-1, 1)
        self._axis_y.setTitleText("Audio level")

        # Add axis
        self._chart.addAxis(self._axis_x, PySide6.QtCore.Qt.AlignBottom)   # Set X axis at the bottom
        self._chart.addAxis(self._axis_y, PySide6.QtCore.Qt.AlignLeft)     # Set Y axis on the left

        # Attach the series to the newly added axes
        self._series.attachAxis(self._axis_x)
        self._series.attachAxis(self._axis_y)

        self._chart.legend().hide()
        audio_device_name = device.description()
        self._chart.setTitle(f"Data from the microphone ({audio_device_name})")

        format_audio = PySide6.QtMultimedia.QAudioFormat()
        format_audio.setSampleRate(self.sr)
        format_audio.setChannelCount(1)
        format_audio.setSampleFormat(PySide6.QtMultimedia.QAudioFormat.UInt8)

        self._audio_input = PySide6.QtMultimedia.QAudioSource(device, format_audio, self)
        self._io_device = self._audio_input.start()
        if self._io_device is None:
            error_message = f"Failed to start audio input for {audio_device_name}"
            PySide6.QtWidgets.QMessageBox.critical(self, "Error", error_message)
            raise RuntimeError(error_message)
        self._io_device.readyRead.connect(self._readyRead)

        self._chart_view = PySide6.QtCharts.QChartView(self._chart)
        self.setCentralWidget(self._chart_view)

        self._buffer = [PySide6.QtCore.QPointF(x, 0) for x in range(self.sample_count)]
        self._series.append(self._buffer)

    def closeEvent(self, event):
        if self._audio_input is not None:
            self._audio_input.stop()
        event.accept()

    @PySide6.QtCore.Slot()
    def _readyRead(self):
        data = self._io_device.readAll()
        available_samples = data.size() // self.resolution

        start = 0
        if (available_samples < self.sample_count):
            # Move existing samples left to make room for the new data
            start = self.sample_count - available_samples
            for s in range(start):
                self._buffer[s].setY(self._buffer[s + available_samples].y())

        # Copy new data into the buffer.
        data_index = 0
        for s in range(start, self.sample_count):
            value = (ord(data[data_index]) - 128) / 128
            self._buffer[s].setY(value)
            data_index = data_index + self.resolution

        # replace the series with the internal buffer
        self._series.replace(self._buffer)


def main():
    args, remaining = parse()
    print(f"{args=}, {remaining=}")

    # Create the application instance
    app = PySide6.QtWidgets.QApplication(remaining)

    input_devices = PySide6.QtMultimedia.QMediaDevices.audioInputs()
    for device in input_devices:
        print(f"{device=}")
        print(f"  description() = {device.description()}")
        print(f"  id() = {device.id()}")
        print(f"  isDefault() = {device.isDefault()}")
        print(f"  mode() = {device.mode()}")
        print(f"  channelConfiguration() = {device.channelConfiguration()}")
        print(f"  maximumSampleRate() = {device.maximumSampleRate()}")
    if not input_devices:
        PySide6.QtWidgets.QMessageBox.warning(None, "audio", "There is no audio input device available.")
        sys.exit(-1)

    main_win = MainWindow(input_devices[0])
    main_win.setWindowTitle("audio")
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 3 // 4
    main_win.resize(size, size)
    main_win.show()

    # Run the application's event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())



