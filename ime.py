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
import PySide6.QtMultimedia


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


# newrel: consider moving this to a data file, e.g. menu.json
application_menu = [
    ('&File',
        [
            'file_new',
            'file_open',
        ]
    ),
    ('&Edit',
        [
            'undo',
            'redo',
        ]
    ),
    ('&View',
        [
            'mixer',
        ]
    ),
    ('&Help',
        [
            'about',
        ]
    ),
]

application_toolbar = [
    'file_open',
    'undo',
    'redo',
]

player_buttons = [
    'player_back',
    'player_forward',
    'player_record',
    'player_play',
    'player_stop',
    'player_pause',
]

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
        self.setWindowIcon(PySide6.QtGui.QIcon('./assets/ime-logo.svg'))

        # Status Bar
        self.status_bar = PySide6.QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        # Process the actions folder to instantiate all actions, attaching them to this window object.
        self.status_bar.showMessage("Loading actions...")
        load_actions(self)
        self.status_bar.showMessage(f"{len(self.attached_actions.keys())} actions loaded.")

        # Menu bar
        self.menu_bar = self.menuBar()
        for menu_name, action_list in application_menu:
            menu = self.menu_bar.addMenu(menu_name)
            for action_name in action_list:
                # newrel: add some way to put a seperator in the menu
                if action_name not in self.attached_actions:
                    print(f"Menu item '{menu_name}: {action_name}' missing module 'actions/{action_name}.py'")
                    menu.addAction(action_name, lambda m=menu_name, a=action_name: print(f"Menu item '{m}: {a}' missing module 'actions/{a}.py'"))
                    continue
                menu.addAction(self.attached_actions[action_name])

        # Tool Bar
        self.toolbar = PySide6.QtWidgets.QToolBar('Main toolbar')
        self.toolbar.setObjectName('MainToolbar')
        self.addToolBar(self.toolbar)
        for action_name in application_toolbar:
            if action_name not in self.attached_actions:
                print(f"Toolbar action '{action_name}' missing module 'actions/{action_name}.py'")
                continue
            self.toolbar.addAction(self.attached_actions[action_name])

        # Track list, or track area

        # Player controls
        self.player = PySide6.QtMultimedia.QMediaPlayer()
        self.audio_output = PySide6.QtMultimedia.QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)  # Set volume with float in range 0.0 to 1.0

        player_row = PySide6.QtWidgets.QHBoxLayout()
        for action_name in player_buttons:
            if action_name not in self.attached_actions:
                print(f"Player button is missing '{action_name}'")
                continue
            button = PySide6.QtWidgets.QPushButton()
            button.setIcon(self.attached_actions[action_name].icon())
            button.clicked.connect(self.attached_actions[action_name].trigger)
            button.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Fixed, PySide6.QtWidgets.QSizePolicy.Fixed)
            player_row.addWidget(button, alignment=PySide6.QtCore.Qt.AlignLeft)

        container = PySide6.QtWidgets.QWidget()
        container.setLayout(player_row)
        self.setCentralWidget(container)

        self.player.setSource("D:/Reaper/Rock of Ages/Rock of Ages.wav")  # bugbug: connect this to whatever the final is or mix to or something...

        # Mixer

        #self.status_bar.showMessage('Integrated Music Environment initialization complete')

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
