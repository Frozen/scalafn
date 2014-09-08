from collections import defaultdict
from functools import wraps
from future.builtins import *  # required!!
import types
from scalafn import Map


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


def _eq_(first, second):
    return first == second


def _bool_(first):
    return bool(first)


class Underscore(object):

    def __init__(self, action, arg):
        self.__action__ = action
        self.__arg__ = arg

    def __mul__(self, other):
        return self.__class__(_mul_, other)

    __rmul__ = _mul_

    def __div__(self, other):
        return self.__class__(_div_, other)

    __truediv__ = __div__

    def __rdiv__(self, other):
        return self.__class__(_rdiv_, other)

    __rtruediv__ = __rdiv__

    def __add__(self, other):
        return self.__class__(_add_, other)

    __radd__ = __add__

    def __sub__(self, other):
        return self.__class__(_sub_, other)

    def __rsub__(self, other):
        return self.__class__(_rsub_, other)

    def __lt__(self, other):
        # print('Underscore __lt__', )
        return self.__class__(_lt_, other)

    def __le__(self, other):
        return self.__class__(_le_, other)

    def __gt__(self, other):
        return self.__class__(_gt_, other)

    def __ge__(self, other):
        return self.__class__(_ge_, other)

    def __getattr__(self, item):
        return AttributeUnderscore(item)

    def __contains__(self, item):
        # print("contains", item)
        raise NotImplementedError

    def __call__(self, value):
        return self.__action__(value, self.__arg__)

    def __iter__(self):
        return iter([1, 2, 3])


class AttributeUnderscore():

    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def __lt__(self, other):
        return AttributeCallUnderscore(_lt_, self.attribute_name, other)

    def __le__(self, other):
        return AttributeCallUnderscore(_le_, self.attribute_name, other)

    def __gt__(self, other):
        return AttributeCallUnderscore(_gt_, self.attribute_name, other)

    def __ge__(self, other):
        return AttributeCallUnderscore(_ge_, self.attribute_name, other)

    def __mul__(self, other):
        return AttributeCallUnderscore(_mul_, self.attribute_name, other)

    def __rmul__(self, other):
        return AttributeCallUnderscore(_mul_, self.attribute_name, other)

    def __div__(self, other):
        return AttributeCallUnderscore(_div_, self.attribute_name, other)

    __truediv__ = __div__

    def __rdiv__(self, other):
        return AttributeCallUnderscore(_rdiv_, self.attribute_name, other)

    __rtruediv__ = __rdiv__

    def __call__(self, *args, **kwargs):
        return MethodUnderscore(self.attribute_name, *args, **kwargs)

    def get_callable(self):
        attribute_name = self.attribute_name

        def AttributeUnderscore_get_callable(obj):
            return getattr(obj, attribute_name)
        return AttributeUnderscore_get_callable

class AttributeCallUnderscore():

    def __init__(self, action, attribute_name, other):
        self.action = action
        self.attribute_name = attribute_name
        self.other = other

    def __call__(self, object):
        ret = self.action(getattr(object, self.attribute_name), self.other)
        return ret


class MethodUnderscore():

    def __init__(self, attribute_name, *args, **kwargs):
        self.attribute_name = attribute_name
        self.args = args
        self.kwargs = kwargs

    def __gt__(self, other):
        return MethodCallUnderscore(_gt_, self.attribute_name, other, *self.args, **self.kwargs)

    def __ge__(self, other):
        return MethodCallUnderscore(_ge_, self.attribute_name, other, *self.args, **self.kwargs)

    def __lt__(self, other):
        return MethodCallUnderscore(_lt_, self.attribute_name, other, *self.args, **self.kwargs)

    def __le__(self, other):
        return MethodCallUnderscore(_le_, self.attribute_name, other, *self.args, **self.kwargs)

    def __eq__(self, other):
        return MethodCallUnderscore(_eq_, self.attribute_name, other, *self.args, **self.kwargs)

    def __mul__(self, other):
        return MethodCallUnderscore(_mul_, self.attribute_name, other, *self.args, **self.kwargs)

    def __rmul__(self, other):
        return MethodCallUnderscore(_mul_, self.attribute_name, other, *self.args, **self.kwargs)

    def __div__(self, other):
        return MethodCallUnderscore(_div_, self.attribute_name, other, *self.args, **self.kwargs)

    def __truediv__(self, other):
        return MethodCallUnderscore(_div_, self.attribute_name, other, *self.args, **self.kwargs)

    def __rtruediv__(self, other):
        return MethodCallUnderscore(_rdiv_, self.attribute_name, other, *self.args, **self.kwargs)

    def __rdiv__(self, other):
        return MethodCallUnderscore(_rdiv_, self.attribute_name, other, *self.args, **self.kwargs)

    def __nonzero__(self):
        return bool(getattr(self.args[0], self.attribute_name))

    def get_callable(self):
        def MethodUnderscore_get_call(obj):
            attr = getattr(obj, self.attribute_name)
            ret = attr(*self.args, **self.kwargs)
            return ret
        return MethodUnderscore_get_call




class MethodCallUnderscore():

    def __init__(self, action, attribute_name, __arg__, *args, **kwargs):
        self.__action__ = action
        self.attribute_name = attribute_name
        self.args = args
        self.kwargs = kwargs
        self.__arg__ = __arg__

    def __call__(self, obj):
        value = getattr(obj, self.attribute_name)(*self.args, **self.kwargs)
        return self.__action__(value, self.__arg__)


call_without_parameters_lambda = lambda first, second: first
_ = Underscore(call_without_parameters_lambda, None)


def need_call(f):

    @wraps(f)
    def d(self, func):
        if isinstance(func, (AttributeUnderscore, MethodUnderscore)):
            func = func.get_callable()
        return f(self, func)

    return d



class ListGenerator(object):

    def __init__(self, gen):
        self._gen = gen

    @need_call
    def map(self, func):
        return ListGenerator(map(func, self._gen))

    def toList(self):
        return List(*list(self._gen))

    def mkString(self, param, start=None, end=None):
        return self.toList().mkString(param, start, end)

    def flatten(self):
        return self.filter(_)

    def filter(self, func):
        return ListGenerator(filter(func, self._gen))

    @need_call
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
            d[tmp] = d[tmp] + List(i)

        return Map(d)


class List(list):

    def __init__(self, *v):
        super(List, self).__init__(v)

    @need_call
    def map(self, func):
        return self.toStream().map(func)

    @need_call
    def filter(self, func):
        return self.toStream().filter(func)



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
        # return repr(self.toList())
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

    @need_call
    def filterNot(self, func):
        n = lambda x: not func(x)
        return self.filter(n)


    def groupBy(self, func):
        return self.toStream().groupBy(func)


class String():

    def __init__(self, s):

        self._s = s if s is not None else ''

    def replace(self, old, new, count=-1):
        return String(self._s.replace(old, new, count))

    def split(self, sep=None, maxsplit=-1):
        return List(*self._s.split(sep, maxsplit))

