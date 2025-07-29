from foyndation import singleton
from inspect import isfunction

@singleton
class outerzip:

    class Session:

        def __init__(self, iterables):
            self.iterators = [iter(i) for i in iterables]

        def row(self):
            self.validrow = len(self.iterators)
            for i in self.iterators:
                try:
                    yield next(i)
                except StopIteration:
                    self.validrow -= 1
                    yield

    def __call__(self, *iterables):
        session = self.Session(iterables)
        while True:
            values = tuple(session.row())
            if not session.validrow:
                break
            yield values

def enum(*lists):
    def d(cls):
        cls.enum = v = []
        for args in lists:
            obj = cls(*args)
            setattr(cls, args[0], obj)
            v.append(obj)
        return cls
    return d

def bfs(keys):
    '''Breadth-first search starting with the given iterable of keys, intended to be used as a decorator.
    If a function is decorated it should take an info object and key, and yield subsequent keys.
    If a class is decorated, a new instance of it is used as info object:
    The class should have a `newdepth` method that will be called before each depth, and a `process` method that takes a key and yields subsequent keys as in the function case.
    The info object is kept updated with the list of `currentkeys`, current `depth` and the set of `donekeys`.
    Note that the first `currentkeys` (`depth` 0) is exactly the passed in `keys` iterable, subsequent `currentkeys` will be non-empty lists.
    The process function is only invoked for keys that have not yet been processed, i.e. unique keys.
    When finished the decorated function/class is replaced with the last state of the info object.'''
    def transform(function_or_class):
        if isfunction(function_or_class):
            class Info:
                def newdepth(self):
                    pass
                def process(self, key):
                    return function_or_class(self, key)
            info = Info()
        else:
            info = function_or_class()
        nextkeys = keys
        info.depth = -1
        info.donekeys = set()
        while True:
            iterator = iter(nextkeys)
            try:
                key = next(iterator)
            except StopIteration:
                break
            info.currentkeys = nextkeys
            info.depth += 1
            info.newdepth()
            nextkeys = []
            while True:
                if key not in info.donekeys:
                    j = info.process(key)
                    if j is not None:
                        nextkeys.extend(j)
                    info.donekeys.add(key)
                try:
                    key = next(iterator)
                except StopIteration:
                    break
        return info
    return transform
