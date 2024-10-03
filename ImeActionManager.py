#!python3
r""" ImeActionManager.py



"""
import pathlib
import importlib
import inspect
from collections.abc import MutableMapping

class ImeActionManager(MutableMapping):
    def __init__(self, parent):
        self._attached_actions = dict()
        self.parent = parent

        # Process the actions folder
        actions_dir = pathlib.Path(__file__).parent / 'actions'
        for action_file in actions_dir.glob('*.py'):
            module_name = action_file.stem
            module = importlib.import_module(f'actions.{module_name}')

            if not hasattr(module, 'attach_action'):
                print(f"Skipped module '{module_name}' as it does not define 'attach_action'.")
                continue
            if not inspect.isfunction(module.attach_action):
                print(f"Skipped module '{module_name}' because 'attach_action' in the module is not a function.")
                continue

            self._attached_actions[module_name] = module.attach_action(parent)

    def __repr__(self):
        return f"ImeActionManager({self.parent=})"

    def __str__(self):
        return f"ImeActionManager({len(self._attached_actions)} attached actions:\n  {'\n  '.join([a for a in self._attached_actions.keys()])})"

    def __getitem__(self, key):
        return self._attached_actions[key]

    def __setitem__(self, key, value):
        self._attached_actions[key] = value

    def __delitem__(self, key):
        del self._attached_actions[key]

    def __iter__(self):
        return iter(self._attached_actions)

    def __len__(self):
        return len(self._attached_actions)

    def __contains__(self, key):
        return key in self._attached_actions

    def keys(self):
        return self._attached_actions.keys()

    def values(self):
        return self._attached_actions.values()

    def items(self):
        return self._attached_actions.items()

    def get(self, key, default=None):
        return self._attached_actions.get(key, default)

    def clear(self):
        self._attached_actions.clear()

    def update(self, *args, **kwargs):
        self._attached_actions.update(*args, **kwargs)

    def setdefault(self, key, default=None):
        return self._attached_actions.setdefault(key, default)

    def pop(self, key, default=None):
        return self._attached_actions.pop(key, default)

    def popitem(self):
        return self._attached_actions.popitem()

    def copy(self):
        new_instance = ImeActionManager.__new__(ImeActionManager)
        new_instance._attached_actions = self._attached_actions.copy()
        return new_instance

