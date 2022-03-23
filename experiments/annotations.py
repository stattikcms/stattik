import inspect

from typing import Union, get_origin, get_args

def f(x: int, y: int | None ) -> int:
    return x + y

a = inspect.get_annotations(f)
print(a)
y = a['y']
print(y)
t = type(y)
print(t)
#print(t.__dict__)
print(get_args(y))
