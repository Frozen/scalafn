from collections import defaultdict
from future.builtins import *  # required!!
import types
from scalafn import Map

class ListGenerator(object):

    def __init__(self, gen):
        self._gen = gen

    def __pos__(self):
        return MultipleAdd(self)

    def map(self, func):
        return ListGenerator(map(func, self._gen))

    def toList(self):
        return List(*list(self._gen))

    def mkString(self, param, start=None, end=None):
        return self.toList().mkString(param, start, end)

    def flatten(self):
        return self.filter(lambda x: x)

    def filter(self, func):
        return ListGenerator(filter(func, self._gen))

    def filterNot(self, func):

        n = lambda x: not func(x)
        return self.filter(n)

    def __eq__(self, other):
        return self.toList() == other

    def __repr__(self):
        return repr(self.toList())

    def __len__(self):
        return self.toList().length()

    def __str__(self):
        return repr(self)

    def length(self):
        return len(self)

    def __iter__(self):
        return iter(self._gen)

    def groupBy(self, func):

        d = defaultdict(List)

        for i in self:
            tmp = func(i)
            # d[tmp] = d[tmp] + i
            d[tmp] += i

        return Map(d)

    def sorted(self, cmp=None, key=None, reverse=False):
        return self.toList().sorted(cmp, key, reverse)


class MultipleAdd():

    def __init__(self, val):
        self.val = val

    def get_val(self):
        return self.val


class List(list):

    def __init__(self, *v):
        super(List, self).__init__(v)

    def map(self, func):
        return self.toStream().map(func)

    def filter(self, func):
        return self.toStream().filter(func)

    def flatten(self):
        return self.filter(lambda x: x)

    def __str__(self):
        return super(List, self).__str__()

    def toList(self):
        return self

    def __eq__(self, other):
        if isinstance(other, List):
            return super(List, self).__eq__(other)
        if isinstance(other, ListGenerator):
            return self == other.toList()
        if isinstance(other, list):
            return super(List, self).__eq__(other)
        return False

    def __repr__(self):
        r = super(List, self).__repr__()
        return "List(" + r.replace("[", "").replace("]", "") + ")"

    def mkString(self, param, start=None, end=None):
        rs = param.join(self.map(str).toList())
        if start is not None:
            rs = str(start) + rs
        if end is not None:
            rs += str(end)
        return rs

    def __pos__(self):
        return +self.toStream()

    def toStream(self):
        return ListGenerator(i for i in self)

    def __add__(self, other):

        if isinstance(other, MultipleAdd):
            values = other.get_val()
            return List(*super(List, self).__add__(values.toList()))

        return List(*super(List, self).__add__([other]))
        # if isinstance(other, list):
        #     return List(*super(List, self).__add__(other))
        # if isinstance(other, (tuple, types.GeneratorType)):
        #     return List(*super(List, self).__add__(list(other)))
        # return List(*super(List, self).__add__([other]))

    def __iadd__(self, other):
        self.append(other)
        return self

    def length(self):
        return len(self)

    def filterNot(self, func):
        return self.toStream().filterNot(func)

    def groupBy(self, func):
        return self.toStream().groupBy(func)

    def sorted(self, cmp=None, key=None, reverse=False):
        return List(*sorted(self, cmp=cmp, key=key, reverse=reverse))

class String():

    def __init__(self, s):

        self._s = s if s is not None else ''

    def replace(self, old, new, count=-1):
        return String(self._s.replace(old, new, count))

    def split(self, sep=None, maxsplit=-1):
        return List(*self._s.split(sep, maxsplit))

