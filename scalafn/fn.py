from functools import partial, wraps
from scalafn import Underscore


__isinstance = isinstance



def _fn(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        args = list(args)

        if any(__isinstance(arg, Underscore) for arg in args) or \
           any(__isinstance(kwargs[index], Underscore) for index in kwargs):
            #  fn.len(_)
            def underscore_call(underscore_param):
                _args = list(args)
                for index, arg in enumerate(_args):
                    if __isinstance(arg, Underscore):
                        _args[index] = underscore_param
                        return f(*_args, **kwargs)
                _kwargs = kwargs.copy()
                for index in _kwargs:
                    if __isinstance(_kwargs[index], Underscore):
                        _kwargs[index] = underscore_param
                        return f(*_args, **_kwargs)
                return f(*_args, **_kwargs)
            return underscore_call
        else:
            # fn.len([]) == 0
            return f(*args, **kwargs)
    wrapper.__need_call__ = True
    return wrapper

underscore_wrapper = _fn


isinstance = underscore_wrapper(__isinstance)

__len = len
len = underscore_wrapper(len)


@underscore_wrapper
def eq(first, second):
    return first == second