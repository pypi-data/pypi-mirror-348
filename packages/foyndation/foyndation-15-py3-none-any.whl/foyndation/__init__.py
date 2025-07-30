from contextlib import contextmanager
import logging

dotpy = '.py'

class Forkable:

    @classmethod
    def _of(cls, *args, **kwargs):
        return cls(*args, **kwargs)

def initlogging():
    'Initialise the logging module to send debug (and higher levels) to stderr.'
    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", level = logging.DEBUG)

class Proxy:

    def __getattr__(self, name):
        try:
            return getattr(self._enclosinginstance, name)
        except AttributeError:
            superclass = super()
            try:
                supergetattr = superclass.__getattr__
            except AttributeError:
                raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
            return supergetattr(name)

def innerclass(cls):
    'An instance of the decorated class may access its enclosing instance via `self`.'
    class InnerMeta(type):
        def __get__(self, enclosinginstance, owner):
            clsname = (cls if self is Inner else self).__name__
            return type(clsname, (Proxy, self), dict(_enclosinginstance = enclosinginstance))
    Inner = InnerMeta('Inner', (cls,), {})
    return Inner

def _rootcontext(e):
    while True:
        c = getattr(e, '__context__', None)
        if c is None:
            return e
        e = c

def invokeall(callables):
    '''Invoke every callable, even if one or more of them fail. This is mostly useful for synchronising with futures.
    If all succeeded return their return values as a list, otherwise raise all exceptions thrown as a chain.'''
    values = []
    failure = None
    for c in callables:
        try:
            obj = c()
        except Exception as e:
            _rootcontext(e).__context__ = failure
            failure = e
        else:
            values.append(obj)
    if failure is None:
        return values
    raise failure

@contextmanager
def onerror(f):
    'Context manager that runs the given function if an exception happens, like `finally` excluding the happy path.'
    try:
        yield
    except:
        f()
        raise

def rmsuffix(text, suffix):
    'Return text with suffix removed, or `None` if text does not end with suffix.'
    if text.endswith(suffix):
        return text[:-len(suffix)]

def singleton(t):
    '''The decorated class is replaced with a no-arg instance.
    Can also be used to replace a factory function with its result.'''
    return t()

def solo(v):
    'Assert exactly one object in the given sequence and return it.'
    x, = v
    return x
