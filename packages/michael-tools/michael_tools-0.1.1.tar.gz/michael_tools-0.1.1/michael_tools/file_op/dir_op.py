import os
from typing import Any


def get_curr_work_dir():
    return os.getcwd()


def get_upper_dir(path=None):
    if path is None:
        path = get_curr_work_dir()
    return os.path.dirname(path)


def path_join(*parts: Any) -> Any:
    if not parts:
        return ""
    first, *rest = parts
    return os.path.join(first, *rest)
