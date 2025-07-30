from weakref import WeakKeyDictionary
import re

lookup = WeakKeyDictionary()
mangledmatch = re.compile('_.*(__.*[^_]_?)').fullmatch

def register(obj, paracls):
    'Instantiate paracls, set `obj` to be the regular object associated with the new parabject, and return the parabject.'
    parabject = paracls()
    lookup[parabject] = obj
    return parabject

class UnknownParabjectException(Exception): pass

def dereference(parabject):
    'Get the regular object associated with `parabject` or raise UnknownParabjectException.'
    try:
        return lookup[parabject]
    except (KeyError, TypeError):
        raise UnknownParabjectException

class Parabject:
    'Subclasses typically implement `__getattr__` for dynamic behaviour on attribute access, use `unmangle` there to undo name mangling.'

    def __neg__(self):
        'Dereference this parabject.'
        return dereference(self)

def unmangle(name):
    'Undo name mangling.'
    return name if (m := mangledmatch(name)) is None else m.group(1)
