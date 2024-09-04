import inspect
import functools
import timeit
import datetime

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
        e_time_rnd = round(exec_time,5)
        timestamp = datetime.datetime.now().timestamp()
        dt = datetime.datetime.fromtimestamp(timestamp)
        with open('calls.log','a+') as file:
            file.write(f"[{dt}][{e_time_rnd}s]{func.__name__}{args}\n")
        return result

    return wrapper

import os

def files_in(path):
  """
  Gets a list of all files in the given path.

  Args:
    path: The path to the directory.

  Returns:
    A list of all files in the directory.
  """

  files = []
  for root, dirs, files in os.walk(path):
    for file in files:
      if os.path.isfile(os.path.join(root, file)):
        files.append(os.path.join(root, file))
  return files
