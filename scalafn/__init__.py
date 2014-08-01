from future.builtins import *
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


def _lt_(first, second):
    return first < second


def _le_(first, second):
    return first <= second


def _gt_(first, second):
    return first > second


def _ge_(first, second):
    return first >= second


def _contains_(first, second):
    return first in second


def _getattr_(obj, item):
    return getattr(obj, item)


class Underscore(object):

    def __init__(self, action, arg):
        self.__action__ = action
        self.__arg__ = arg

    def __mul__(self, other):
        return Underscore(_mul_, other)

    __rmul__ = _mul_

    def __div__(self, other):
        return Underscore(_div_, other)

    __truediv__ = __div__

    def __rdiv__(self, other):
        return Underscore(_rdiv_, other)

    __rtruediv__ = __rdiv__

    def __add__(self, other):
        return Underscore(_add_, other)

    __radd__ = __add__

    def __sub__(self, other):
        return Underscore(_sub_, other)

    def __rsub__(self, other):
        return Underscore(_rsub_, other)

    def __lt__(self, other):
        return Underscore(_lt_, other)

    def __le__(self, other):
        return Underscore(_le_, other)

    def __gt__(self, other):
        return Underscore(_gt_, other)

    def __ge__(self, other):
        return Underscore(_ge_, other)

    def __getattr__(self, item):
        # print('__getattr__', item)
        return Underscore(_getattr_, item)

    def contains(self, item):
        __action__ = lambda first, second: second in first
        return Underscore(__action__, item)

    def in_(self, item):
        __action__ = lambda first, second: first in second
        return Underscore(__action__, item)

    def __contains__(self, item):
        print("contains", item)
        raise NotImplementedError

    def __call__(self, value):
        return self.__action__(value, self.__arg__)

    def __iter__(self):
        return iter([1, 2, 3])


call_without_parameters_lambda = lambda first, second: first
_ = Underscore(call_without_parameters_lambda, None)


class ListGenerator(object):

    def __init__(self, gen):
        self._gen = gen

    def map(self, func):
        if hasattr(func, '__need_call__'):
            func = func(_)
        return ListGenerator(map(func, self._gen))

    def toList(self):
        return List(*list(self._gen))

    def mkString(self, param, start=None, end=None):
        return self.toList().mkString(param, start, end)

    def flatten(self):
        return self.filter(_)

    def filter(self, func):
        return ListGenerator(filter(func, self._gen))

    def __eq__(self, other):
        return self.toList() == other

    def __repr__(self):
        return self.mkString(', ', "ListGenerator(i for i in [", "])")

    def __len__(self):
        return self.toList().length()

    def length(self):
        return len(self)


class List(list):

    def __init__(self, *v):
        super(List, self).__init__(v)

    def map(self, func):
        if hasattr(func, '__need_call__'):
            func = func(_)
        return ListGenerator(map(func, self))

    def filter(self, func):
        return ListGenerator(filter(func, self))

    def flatten(self):
        return self.filter(_)

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

    def length(self):
        return len(self)


class String():

    def __init__(self, s):

        self._s = s if s is not None else ''

    def replace(self, old, new, count=-1):
        return String(self._s.replace(old, new, count))

    def split(self, sep=None, maxsplit=-1):
        return List(*self._s.split(sep, maxsplit))

