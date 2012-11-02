from numba import *

@autojit
def error1():
    def inner():
        pass

@autojit
def error2():
    @autojit
    def inner():
        pass

@autojit
def error3():
    inner(10, 20, 30)

    @jit(restype=void, argtypes=[int_, int_, int_])
    def inner(a, b, c):
        print a, b, c

@autojit
def error4():
    @jit(restype=void, argtypes=[int_, int_, int_])
    def inner(a, b, c):
        print a, b, c

    inner(10, a=20, b=30, c=40)

@autojit
def error5():
    @jit(restype=void, argtypes=[int_, int_, int_])
    def inner(a, b, c):
        print a, b, c

    inner(10, a=20, b=30)

@autojit
def closure1():
    a = 10
    @jit(restype=void, argtypes=[int_])
    def inner(arg):
        print arg

    return inner

@autojit
def closure2():
    a = 10
    @jit(restype=void, argtypes=[int_])
    def inner(arg):
        print arg

    inner(arg=a)

@autojit
def closure3():
    a = 10

    @jit('void()')
    def inner():
        print a

    a = 12
    inner()

@autojit
def closure4():
    a = 10

    @jit('void()')
    def inner():
        print a

    a = 12
    return inner

@autojit
def nested_closure():
    a = 20
    b = 21

    @jit('object_()')
    def c1():
        b = 10
        @jit('void()')
        def c2():
            print a, b

        return c2

    @jit('void()')
    def c3():
        print b

    return c1, c3

__doc__ = """
>>> error1()
Traceback (most recent call last):
    ...
NumbaError: 5:4: Closure must be decorated with 'jit' or 'autojit'
>>> error2()
Traceback (most recent call last):
    ...
NumbaError: 10:5: Dynamic closures not yet supported, use @jit
>>> error3()
Traceback (most recent call last):
    ...
UnboundLocalError: inner
>>> error4()
Traceback (most recent call last):
    ...
NumbaError: 28:4: Expected 3 arguments, got 4
>>> error5()
Traceback (most recent call last):
    ...
NumbaError: Got multiple values for positional argument 'a'

Test closures

>>> closure1().__name__
'inner'
>>> closure1()()
Traceback (most recent call last):
    ...
TypeError: function takes exactly 1 argument (0 given)
>>> closure1()(object())
Traceback (most recent call last):
    ...
TypeError: an integer is required
>>> closure1()(10.0)
10
>>> closure2()
10
>>> closure3()
12
>>> func = closure4()
>>> print func.__name__
inner
>>> print func.__closure__._numba_attrs._fields_
[('__numba_scope_a', <class 'ctypes.c_int'>)]
>>> print func.__closure__._numba_attrs.__numba_scope_a
12
>>> func()
12

>>> c1, c3 = nested_closure()
>>> c1.__name__
'c1'
>>> c3.__name__
'c3'
>>> c1().__name__
'c2'
>>> c1()()
20 10
>>> c3()
21
"""

if __name__ == '__main__':
#    c1, c3 = nested_closure()
#    print c1.__name__, c3.__name__
    import doctest
    doctest.testmod()