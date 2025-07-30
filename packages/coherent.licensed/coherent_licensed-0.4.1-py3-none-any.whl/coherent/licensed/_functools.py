import functools


# from jaraco.functools 4.1
def compose(*funcs):
    def compose_two(f1, f2):
        return lambda *args, **kwargs: f1(f2(*args, **kwargs))

    return functools.reduce(compose_two, funcs)


def apply(transform):
    def wrap(func):
        return functools.wraps(func)(compose(transform, func))

    return wrap
