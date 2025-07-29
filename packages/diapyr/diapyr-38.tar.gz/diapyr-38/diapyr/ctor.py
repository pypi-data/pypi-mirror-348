def isctormethod(m):
    return hasattr(m, 'di_deptypes') and not hasattr(m, 'di_owntype')

class Constructor:

    def __init__(self, invoke, method):
        self.invoke = invoke
        self.method = method

class RegularConstructor(Constructor):

    @classmethod
    def find(cls, clazz):
        m = clazz.__init__
        if isctormethod(m):
            yield cls(clazz, m)

class CustomConstructor(Constructor):

    @classmethod
    def find(cls, clazz):
        for name in dir(clazz):
            m = getattr(clazz, name)
            if getattr(m, '__self__', None) is clazz and isctormethod(m):
                yield cls(m, m)
