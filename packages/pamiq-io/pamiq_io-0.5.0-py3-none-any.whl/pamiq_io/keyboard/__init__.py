import sys

from .output import Key, KeyboardOutput

__all__ = ["Key", "KeyboardOutput"]

if sys.platform == "linux":
    try:
        from .output.inputtino import InputtinoKeyboardOutput

        __all__.extend(["InputtinoKeyboardOutput"])
    except ModuleNotFoundError:
        pass

if sys.platform == "win32":
    try:
        from .output.directinput import DirectInputKeyboardOutput

        __all__.extend(["DirectInputKeyboardOutput"])
    except ModuleNotFoundError:
        pass
