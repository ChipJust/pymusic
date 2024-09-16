#!python3
r""" FileBrowser.py


"""
import argparse
import pathlib
import sys

import PySide6.QtWidgets


class QWidgetWindow(PySide6.QtWidgets.QWidget):
    def __init__(self, title="File Dialog", default_dir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.default_dir = default_dir if default_dir else pathlib.Path(__file__).parent

        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 100)

        layout = PySide6.QtWidgets.QGridLayout()
        self.setLayout(layout)

        # file selection
        file_browse = PySide6.QtWidgets.QPushButton('Browse')
        file_browse.clicked.connect(self.open_file_dialog)
        self.filename_edit = PySide6.QtWidgets.QLineEdit()

        layout.addWidget(PySide6.QtWidgets.QLabel('File:'), 0, 0)
        layout.addWidget(self.filename_edit, 0, 1)
        layout.addWidget(file_browse, 0 ,2)

    def open_file_dialog(self):
        filename, ok = PySide6.QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(self.default_dir),
            "Any File Type (*.*);;Python (*.py);;Json (*.json)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit.setText(str(path))


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

    qwindow = QWidgetWindow()
    qwindow.show()

    # Run the application's event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
