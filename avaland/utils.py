def test_attr(*args):
    def decorator(func):
        for i in args:
            setattr(func, 'test', i)
        return func
    return decorator
