import inspect
import functools

def log_call(func):
    """Decorator that logs the call to the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #caller_frame = inspect.currentframe().f_back
        #caller_func = caller_frame.f_code.co_name
        with open('calls.log','a+') as file:
            file.write(f"{func.__name__}({args})\n")
        return func(*args, **kwargs)
    return wrapper
