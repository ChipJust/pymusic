#!python3
r""" ime.py - Integrated Music Environment


In case you need to store some app data not using QSettings
    app_dir = pathlib.Path(platformdirs.user_data_dir(
        appname=APPLICATION_TLA,
        appauthor=False,
        ensure_exists=True))
You may want to use this to download https://github.com/adactio/TheSession-data

"""
import platformdirs
import argparse
import pathlib
import sys
import importlib
import inspect

import PySide6.QtWidgets
import PySide6.QtGui
import PySide6.QtCore

# The application three letter acronymn is used to prefix classes and serves as
# the public name, pronounced "i me" sort of like pronouns
APPLICATION_TLA = "ime"
APPLICATION_TITLE = "Integrated Music Environment"


def load_actions(parent):
    if not hasattr(parent, 'attached_actions'):
        parent.attached_actions = dict()

    # Define the directory path for the actions folder relative to the current file
    actions_dir = pathlib.Path(__file__).parent / 'actions'

    # Iterate over all Python files in the actions directory
    for action_file in actions_dir.glob('*.py'):
        module_name = action_file.stem
        module = importlib.import_module(f'actions.{module_name}')

        # Check if the module is a valid action module.
        if not hasattr(module, 'attach_action'):
            print(f"Skipped module '{module_name}' as it does not define 'attach_action'.")
            continue
        if not inspect.isfunction(module.attach_action):
            print(f"Skipped module '{module_name}' because 'action_name' in the module is not a function.")
            continue

        parent.attached_actions[module_name] = module.attach_action(parent)


class imeMainWindow(PySide6.QtWidgets.QMainWindow):
    title = APPLICATION_TITLE
    initial_width = 600
    initial_height = 200

    def __init__(self, default_dir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_dir = default_dir if default_dir else pathlib.Path(__file__).parent
        print(f"{self.default_dir=}")

        # Initialize settings
        self.settings = PySide6.QtCore.QSettings(APPLICATION_TLA, APPLICATION_TLA)

        # Restore geometry and state
        self.restore_settings()

        # Set the title bar
        self.setWindowTitle(self.title)
        self.setWindowIcon(PySide6.QtGui.QIcon('./assets/eigth_rest_icon2.svg'))

        # Menu bar
        self.menu_bar = self.menuBar()

        # Process the actions folder to instantiate all actions, attaching them to this window object.
        load_actions(self)
        print(f"{self.attached_actions.keys()=}")


        # File menu
        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction('New File', lambda: print('File: New File')) # bugbug: todo
        self.file_menu.addAction(self.attached_actions['open_file'])

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
        self.toolbar.setObjectName('MainToolbar')
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.attached_actions['open_file'])

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
