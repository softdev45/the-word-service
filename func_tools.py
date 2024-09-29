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

def gen_book_map():
    result = []
    with open('books') as file:
        while l := file.readline().strip():
            result.append(l)
    return result

def xpath_range(attr, selection: list):
    ranges = []
    if not selection:
        return ''
    for item in selection:
        if type(item) is int:
            ranges.append( f"(@{attr} = {item})")
        elif len(item) == 2:
            start = item[0]
            end = item[1]
            ranges.append( f"(@{attr} >= {start} and @{attr} <= {end})" )
    ranges = ' or '.join(ranges)
    return f"[{ranges}]"

def last_prefixed(lst, chars):
    """
    Finds the last element in a list that starts with the given character.

    Args:
        lst: The input list.
        char: The character to search for at the beginning of elements.

    Returns:
        The last element starting with the given character, or None if not found.
    """

    for i in range(len(lst) - 1, -1, -1):
        if lst[i][0] in chars:
            return lst[i]
    return None


import os

def files_in(path):
    """
    Gets a list of all files in the given path.

    Args:
    path: The path to the directory.

    Returns:
    A list of all files in the directory.
    """
    #path = os.path.abspath(path)
    files = []
    try:
        for file_path in os.listdir(path):
            full_path = os.path.join(path, file_path)
            if os.path.isfile(full_path):
                files.append(full_path)
    except:
        print('could not load from: ', path)
    return files

def files_in2(path):
  w = os.walk(path, topdown=True)
  for (root, dirs, files) in w:
    dirs.clear()
    print(root)
    print(files)
    input()
    for file in files:
      print(file)
      if os.path.isfile(os.path.join(root, file)):
        files.append(os.path.join(root, file))
    input()
  return files
