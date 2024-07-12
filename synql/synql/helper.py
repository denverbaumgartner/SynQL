# system packages 
import os
import contextlib
from typing import Dict
from types import SimpleNamespace

# internal packages

# external packages

def validate_system_path(system_path: str) -> bool:
    """Validate a system path.

    :param path: A system path.
    :type path: str
    :return: Whether the path is valid.
    :rtype: bool
    """
    if not os.path.exists(system_path):
        raise ValueError("Invalid path: {}".format(system_path))
    
@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = os.dup(1)
        old_stderr = os.dup(2)
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)
        try:
            yield
        finally:
            os.dup2(old_stdout, 1)
            os.dup2(old_stderr, 2)
            os.close(old_stdout)
            os.close(old_stderr)

def dict_to_sns(data) -> SimpleNamespace:
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_sns(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_sns(item) for item in data]
    else:
        return data
