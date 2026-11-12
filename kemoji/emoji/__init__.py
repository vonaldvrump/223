"""Registry of all emoji in the pack (in sheet order)."""
import importlib
import pkgutil


def modules():
    mods = []
    for info in pkgutil.iter_modules(__path__):
        if info.name.startswith("e") and info.name[1:4].isdigit():
            mods.append(importlib.import_module(__name__ + "." + info.name))
    mods.sort(key=lambda m: m.__name__)
    return mods


def ident(mod):
    """'101_diamond' style id."""
    return mod.__name__.rsplit(".", 1)[1][1:4] + "_" + mod.NAME
