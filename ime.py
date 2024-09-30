#!python3
r""" ime.py - Integrated Music Environment



In case you need to store some app data not using QSettings
    import platformdirs
    app_dir = pathlib.Path(platformdirs.user_data_dir(
        appname=APPLICATION_TLA,
        appauthor=False,
        ensure_exists=True))
You may want to use this to download https://github.com/adactio/TheSession-data


import PySide6.QtWidgets
import PySide6.QtGui
import PySide6.QtCore
import PySide6.QtMultimedia

"""

# Standard Imports
import argparse
import pathlib
import sys
import importlib
import inspect

# Thrid party imports
import PySide6
import PySide6.QtWidgets
import PySide6.QtMultimedia

# Our imports
import ImeMixerView


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

SEPARATOR = '-'
application_toolbar = [
    'undo',
    'redo',
    SEPARATOR,
    'mixer',
]


class imeMainWindow(PySide6.QtWidgets.QMainWindow):
    title = APPLICATION_TITLE
    initial_width = 600
    initial_height = 200

    def __init__(self, default_dir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_dir = default_dir if default_dir else pathlib.Path(__file__).parent
        print(f"{self.default_dir=}")

        # Track list
        self.tracks = list()

        # Initialize settings
        self.settings = PySide6.QtCore.QSettings(APPLICATION_TLA, APPLICATION_TLA)

        # Restore geometry and state
        self.restore_settings()

        # newrel: make a project data structure to save information about the
        #         project. The settings should just hold a pointer to the last
        #         project, which we should open here if no project was passed
        #         in the constructor, by the way we should replace default_dir
        #         with this project name and make the default directory be the
        #         directory of the project file.

        # newrel: update the cli such that we can register a file association
        #         with the project file's extension, pass the filename into
        #         this script and forward that information to the constructor
        #         such that the user can double-click the project file to open
        #         the project to its current state.

        # Set the title bar
        self.setWindowTitle(self.title)
        self.setWindowIcon(PySide6.QtGui.QIcon('./assets/ime-logo.svg'))
        # newrel: make the pin menu icon use ime-logo

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
            if action_name == SEPARATOR:
                self.toolbar.addSeparator()
                continue
            if action_name not in self.attached_actions:
                print(f"Toolbar action '{action_name}' missing module 'actions/{action_name}.py'")
                continue
            self.toolbar.addAction(self.attached_actions[action_name])

        # Central Widget is between the toolbar and the status bar
        # This is the content area for the application.
        self.content = PySide6.QtWidgets.QStackedWidget()
        self.setCentralWidget(self.content)
        # now add the pages in...each page or view is a widget
        self.mixer_view = ImeMixerView.ImeMixerView(self)
        # newrel: add something to manage view constructors and add the rest of the views
        #         update the mixer action to switch to the mixer_view index in the stack
        self.content.addWidget(self.mixer_view)



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
