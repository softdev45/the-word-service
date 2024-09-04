import inspect
import functools
import timeit

def log_call(func):
    """Decorator that logs the call to the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #caller_frame = inspect.currentframe().f_back
        #caller_func = caller_frame.f_code.co_name
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        exec_time = end_time - start_time
        with open('calls.log','a+') as file:
            file.write(f"[{exec_time}]{func.__name__}({args})\n")

    return wrapper
