from functools import wraps
from future.builtins import *  # required!!
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

