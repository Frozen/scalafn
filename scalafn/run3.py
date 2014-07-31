from functools import partial
import types


def _mul_(first, second):
    return first*second


def _div_(first, second):
    return first/second


def _rdiv_(first, second):
    return second/first


def _add_(first, second):
    return first + second


def _sub_(first, second):
    return first - second


def _rsub_(first, second):
    return second - first

class Underscore(object):

    __action__ = None
    __arg__ = None

    def __mul__(self, other):
        self.__arg__ = other
        self.__action__ = _mul_
        return self

    __rmul__ = _mul_

    def __div__(self, other):
        self.__action__ = _div_
        self.__arg__ = other
        return self

    def __rdiv__(self, other):
        self.__action__ = _rdiv_
        self.__arg__ = other
        return self

    def __add__(self, other):
        self.__action__ = _add_
        self.__arg__ = other
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self.__action__ = _sub_
        self.__arg__ = other
        return self

    def __rsub__(self, other):
        self.__action__ = _rsub_
        self.__arg__ = other
        return self

    def __call__(self, value):
        return self.__action__(value, self.__arg__)

_ = Underscore()


class ListGenerator(object):

    def __init__(self, gen):
        self._gen = gen
        # self._ge/

    def map(self, func):
        return ListGenerator(map(func, self._gen))

    def toList(self):
        return List(*list(self._gen))

    def mkString(self, param, start=None, end=None):
        return self.toList().mkString(param, start, end)

    def __eq__(self, other):
        return self.toList() == other

    def __repr__(self):
        return self.mkString(', ', "ListGenerator(i for i in [", "])")


# class List(list):
class List(list):

    def __init__(self, *v):
        self._v = list(v)
        super(List, self).__init__(v)

    def map(self, func):
        return ListGenerator(map(func, self._v))

    def filter(self, func):
        return ListGenerator(filter(func, self._v))

    def flatten(self):
        return List(*list(filter(lambda x: x, self._v)))

    def __str__(self):
        return str(self._v)

    def toList(self):
        return self

    def __eq__(self, other):
        if isinstance(other, List):
            return self._v == other._v
        if isinstance(other, ListGenerator):
            return self == other.toList()
        if isinstance(other, list):
            return list(self._v) == other
        return False

    def __repr__(self):
        return "List(" + repr(self._v).replace("[", "").replace("]", "") + ")"

    def mkString(self, param, start=None, end=None):
        rs = param.join(self.map(str).toList())
        if start is not None:
            rs = str(start) + rs
        if end is not None:
            rs += str(end)
        return rs

    def __pos__(self):
        return self.toStream()

    def toStream(self):
        return ListGenerator(i for i in self)

    def __add__(self, other):
        if isinstance(other, ListGenerator):
            return List(*super(List, self).__add__(other.toList()))
        if isinstance(other, list):
            return List(*super(List, self).__add__(other))
        if isinstance(other, (tuple, types.GeneratorType)):
            return List(*super(List, self).__add__(list(other)))
        return List(*super(List, self).__add__([other]))



class String():

    def __init__(self, s):

        self._s = s if s is not None else ''

    def replace(self, old, new, count=-1):
        return String(self._s.replace(old, new, count))

    def split(self, sep=None, maxsplit=-1):
        return List(*self._s.split(sep, maxsplit))