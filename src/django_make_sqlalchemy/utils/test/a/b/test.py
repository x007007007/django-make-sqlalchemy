import inspect

def a():
    from .ttt import b
    print(inspect.getmodule(b))
    return b