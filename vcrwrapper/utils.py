import functools

def dual_decorator(func):
    """This is a decorator that converts a paramaterized decorator for no-param use."""
    # modified from http://stackoverflow.com/a/10288927/1231454.
    
    @functools.wraps(func)
    def inner(*args, **kw):
        if ((len(args) == 1 and not kw and callable(args[0])
             # Exceptions are callable; the next line allows us to accept them as args.
             and not (type(args[0]) == type and issubclass(args[0], BaseException)))):
            return func()(args[0])
        else:
            return func(*args, **kw)
    return inner
