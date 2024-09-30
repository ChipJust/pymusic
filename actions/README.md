This folder contains all the actions for the application.

Each file in this folder process by the main application

* import the file
* call a module level function, attach_action(parent)

The action module must

* Create an action
* Add the function that the action corresponds with to the parent object
* add the action to the parent's menu

Template action. Replace action_name with the name of the new action.
```
#!python3
r""" action_name.py



"""
import PySide6.QtGui


def attach_action(parent):
    a = PySide6.QtGui.QAction(
        PySide6.QtGui.QIcon('./assets/action_name.svg'),
        'action_name',
        parent)
    #a.setShortcut('Ctrl+P')
    parent.action_name = action_name.__get__(parent)
    a.triggered.connect(parent.action_name)
    return a


def action_name(self):
    print(f"action_name")
    # bugbug: do action_name

```
