import inspect
from test.a.b import test as t


def get_func_import_info(func):
    assert callable(func)
    module = inspect.getmodule(func)
    return module, func.__name__


print(get_func_import_info(t.a()))