import uuid
import traceback
import importlib.util
from pathlib import Path
from functools import lru_cache, wraps
from typing import Any, TypeAlias, Literal, Callable, Union, Optional
from .types import is_array, is_dict, is_number, is_string, is_float, is_int
from .backbones.misc.json_call_tools import (
    CommandInterpreter,
    Command,
    ReturnConfig,
    Action,
)


def percentage_difference(num1: int | float, num2: int | float):
    """
    Calculate the percentage difference between two numbers.

    Parameters:
    - num1 (float): The first number.
    - num2 (float): The second number.

    Returns:
    float: The percentage difference.
    """
    assert (
        num1 != 0
    ), "Cannot calculate percentage difference when the first number is zero."

    percentage_difference = ((num2 - num1) / num1) * 100
    return abs(percentage_difference)


def flatten_list(entry):
    """
    Example:
    ```py
    from gr1336_toolbox import flatten_list

    sample = ["test", [[[1]], [2]], 3, [{"last":4}]]
    results = flatten_list(sample)
    # results = ["test", 1, 2, 3, {"last": 4}]
    ```"""
    if is_array(entry):
        return [item for sublist in entry for item in flatten_list(sublist)]
    return [entry] if entry is not None else []


def filter_list(
    entry: Union[list, tuple], types: Union[TypeAlias, tuple[TypeAlias]]
) -> list:
    assert is_array(
        entry, allow_empty=True
    ), "To filter a list, it must be a list or a tuple"
    return [x for x in entry if isinstance(x, types)]


def ff_list(entry: Union[list, tuple], types: Union[TypeAlias, tuple[TypeAlias]]):
    """Flattens and filters the provided list"""
    assert is_array(
        entry, allow_empty=True
    ), "To flatten and filter a list, it must be a list or a tuple"
    return filter_list(flatten_list(entry), types)


def try_call(comp: Callable, verbose_exception: bool = False, *args, **kwargs):
    """Can be used to call a function prune to errors, it returns its response if successfuly executed, otherwise it prints out an traceback if verbose_exception.

    Args:
        comp (Callable): _description_
        verbose_exception (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    try:
        return comp(*args, **kwargs)
    except Exception as e:
        if verbose_exception:
            print(f"Exception: '{e}'. Traceback:")
            traceback.print_exc()
        return None


def import_functions(
    path: Union[str, Path],
    target_function: str,
    pattern: str = "*.py",
    scan_type: Literal["glob", "rglob"] = "rglob",
):
    """
    Imports and returns all functions from .py files in the specified directory matching a certain function name.

    Args:
        path (str or Path): The path of the directories to search for the Python files.
        target_function (str): The exact string representing the function name to be searched within each file.
        pattern (str, optional): Pattern of the file to be scanned. Defaults to "*.py" with covers all files with .py extension.
        scan_type (Literal["glob", "rglob"], optional): uses either glob or rglob to scan for the files within the directory. 'rglob' does a deeper scan, into the directory and sub-directory, while 'glob' will do the scan on the directory only.

    Returns:
        list: A list containing all the functions with the given name found in the specified directory and subdirectories.

    Example:
        >>> import_functions('/path/to/directory', 'some_function')
        [<function some_function at 0x7f036b4c6958>, <function some_function at 0x7f036b4c69a0>]
    """
    results = []
    if not Path(path).exists():
        return results
    if Path(path).is_dir():
        if scan_type == "rglob":
            python_files = [x for x in Path(path).rglob(pattern) if x.is_file()]
        else:
            python_files = [x for x in Path(path).glob(pattern) if x.is_file()]
    else:
        python_files = [path]
    for file in python_files:
        spec = importlib.util.spec_from_file_location(file.name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, target_function):
            results.append(getattr(module, target_function))
    return results


def sort_array(array: list | tuple, reverse: bool = False):
    """
    Sorts a list of tuples based on the first element of each tuple.

    Args:
        imports (list of tuple): A list where each element is a tuple,
                                 with the first element being a string or integer.

    Returns:
        list of tuple: The sorted list of import tuples.

    Example:
        >>> sort_imports([(3, 'bar'), (1, 'foo'), (2, 'baz')])
        [(1, 'foo'), (2, 'baz'), (3, 'bar')]
    """
    if is_array(array, allow_empty=False):
        return sorted(array, key=lambda x: x[0], reverse=reverse)
    return array


def process_number(
    value: int | float | str | Any,
    default_value: int | float | Any | None = None,
    minimum: int | float | None = None,
    maximum: int | float | None = None,
    return_type: Literal["int", "float"] = None,
) -> int | float | Any:
    """Process a number while constraining it

    Args:
        value (int | float | str | Any): _description_
        default_value (int | float | Any | None, optional): _description_. Defaults to None.
        minimum (int | float | None, optional): _description_. Defaults to None.
        maximum (int | float | None, optional): _description_. Defaults to None.
        return_type (Literal[&quot;int&quot;, &quot;float&quot;], optional): _description_. Defaults to None.

    Returns:
        int | float | Any: _description_
    """
    if not is_number(value, True):
        return default_value

    if is_string(value, strip_string=True):
        value = str(value).strip()
        if is_float(value, True):
            try:
                value = float(value)
            except ValueError:
                return default_value

    if is_int(minimum, True):
        value = max(value, int(minimum))
    elif is_float(minimum, True):
        value = max(value, float(minimum))

    if is_int(maximum, True):
        value = min(value, int(maximum))
    elif is_float(maximum, True):
        value = min(value, float(maximum))

    return (
        value
        if return_type is None
        else float(value) if return_type == "float" else int(value)
    )


def remove_file_extension(
    file_name: Union[str, Path], default_file_name: Optional[str] = None
) -> str:
    """Remove the extension from a given file_name. If filename is not valid, then it tries to use default_file_name.
    If both are invalid, it returns a random uuid4 in string format (not hex).

    Args:
        file_name (str | Path): _description_
        default_file_name (str | None, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    assert is_string(file_name), "file_name must be valid!"
    if is_string(file_name, False, True):
        return Path(file_name).stem
    elif is_string(default_file_name, False, True):
        return str(default_file_name)
    return str(uuid.uuid4())


def cache_wrapper(func):
    """
    A decorator to cache the function result while keeping the original documentation, variable names, etc.

    Example
        ```py
        @cache_wrapper
        def your_function(arg1:int, arg2:int) -> bool:
            \"\"\"
            compares if the first number is larger than the second number.
            args:
                arg1(int): The number that is expected to be larger than arg2.
                arg2(int): The number expected to be smaller than arg1

            return:
                bool: True if arg1 is larger than arg2 otherwise False.
            \"\"\"
            return arg1 > arg2
        ```
    """
    cached_func = lru_cache(maxsize=None)(func)

    # Apply the wraps decorator to copy the metadata from the original function
    @wraps(func)
    def wrapper(*args, **kwargs):
        return cached_func(*args, **kwargs)

    return wrapper
