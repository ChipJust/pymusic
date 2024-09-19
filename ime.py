#!python3
r""" ime.py - Integrated Music Environment


In case you need to store some app data not using QSettings
    app_dir = pathlib.Path(platformdirs.user_data_dir(
        appname=APPLICATION_TLA,
        appauthor=False,
        ensure_exists=True))
You may want to use this to download https://github.com/adactio/TheSession-data

We need a way to manage actions modularly
    Seems like each action is global to the application
    But the data the the action manipulates is not always defined close to the manipulation
    And the tendency is for the action to be a method of the main window's class, which is going to lead to a very large class...
    How can we put each action in its own file and integrate them into the main class
    Adding the action to the correct menu also seems like coupling to me

"""
import platformdirs
import argparse
import pathlib
import sys

import PySide6.QtWidgets
import PySide6.QtGui
import PySide6.QtCore

# The application three letter acronymn is used to prefix classes and serves as
# the public name, pronounced "i me" sort of like pronouns
APPLICATION_TLA = "ime"
APPLICATION_TITLE = "Integrated Music Environment"


class imeMainWindow(PySide6.QtWidgets.QMainWindow):
    title = APPLICATION_TITLE
    initial_width = 600
    initial_height = 200

    def __init__(self, default_dir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_dir = default_dir if default_dir else pathlib.Path(__file__).parent

        # Initialize settings
        self.settings = PySide6.QtCore.QSettings(APPLICATION_TLA, APPLICATION_TLA)

        # Restore geometry and state
        self.restore_settings()

        # Set the title bar
        self.setWindowTitle(self.title)
        self.setWindowIcon(PySide6.QtGui.QIcon('./assets/eigth_rest_icon2.svg'))

        # Menu bar
        self.menu_bar = self.menuBar()

        # File menu
        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction('New File', lambda: print('File: New File')) # bugbug: todo

        open_action = PySide6.QtGui.QAction(PySide6.QtGui.QIcon('./assets/arrow-down-from-arc.svg'), 'File: Open File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file_dialog)
        #self.filename_edit = PySide6.QtWidgets.QLineEdit() # used in open_file_dialog
        self.file_menu.addAction(open_action)

        # Edit menu
        self.edit_menu = self.menu_bar.addMenu('&Edit')
        self.edit_menu.addAction('Undo', lambda: print('Edit: Undo')) # bugbug: todo
        self.edit_menu.addAction('Redo', lambda: print('Edit: Redo')) # bugbug: todo

        # View menu
        self.view_menu = self.menu_bar.addMenu('&View')
        self.view_menu.addAction('Mixer', lambda: print('View: Mixer')) # bugbug: todo

        # Help menu
        self.help_menu = self.menu_bar.addMenu('&Help')
        self.help_menu.addAction('About', lambda: print('Help: About')) # bugbug: todo

        # Tool Bar
        self.toolbar = PySide6.QtWidgets.QToolBar('Main toolbar')
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(open_action)

        # Status Bar
        self.status_bar = PySide6.QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Integrated Music Environment initialization complete')

    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def restore_settings(self):
        geometry = self.settings.value("geometry")
        state = self.settings.value("windowState")
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)
        if not geometry and not state:
            self.resize(self.initial_width, self.initial_height)
            self.showMaximized()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def open_file_dialog(self):
        filename, ok = PySide6.QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select a File",
            str(self.default_dir),
            "Any File Type (*.*);;Python (*.py);;Json (*.json)"
        )
        print(f"{filename=}, {ok=}")
        path = pathlib.Path(filename)
        #if filename:
        #    path = pathlib.Path(filename)
        #    #self.filename_edit.setText(str(path))
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

def parse():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    return parser.parse_known_args()


def main():
    args, remaining = parse()
    print(f"{args=}, {remaining=}")

    # Create the application instance
    app = PySide6.QtWidgets.QApplication(remaining)

    ime = imeMainWindow()
    ime.show()

    # Run the application's event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
