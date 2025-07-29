import warnings
from pathlib import Path
from typing import (
    Any,
    Literal,
    Union,
    TypeGuard,
    TypeVar,
    Optional,
    Sequence,
    TypeAlias,
    Type,
    List,
    Tuple,
    Dict,
)


try:
    from torch import Tensor  # type: ignore

    _has_torch = True
except ModuleNotFoundError:
    _has_torch = False

try:
    from numpy import ndarray  # type: ignore

    _has_numpy = True
except ModuleNotFoundError:
    _has_numpy = False


T = TypeVar("T")

NUMBER: TypeAlias = Union[int, float]


def is_numpy(entry: Any, verbose_warn: bool = False) -> TypeGuard[T]:
    if not _has_numpy:
        if verbose_warn:
            warnings.warn(
                "You dont have numpy installed, the response will be always False"
            )
        return False
    return isinstance(entry, ndarray)


def is_tensor(entry: Any, verbose_warn: bool = False) -> TypeGuard[T]:
    if not _has_torch:
        if verbose_warn:
            warnings.warn(
                "You dont have torch installed, the response will be always False"
            )
        return False
    return isinstance(entry, Tensor)


def is_float(entry: Any, check_string: bool = False) -> TypeGuard[float]:
    """
    Checks if the entry provided is a valid float. It can check if a string can be converted to float if check_string is True.

    Args:
        entry (Any): The value to be checked.
        check_string (bool, optional): If True, it will check if the value can be converted to float.

    Returns:
        bool: If True, means that is a valid float otherwise false.
    """
    if isinstance(entry, float):
        return True
    if not check_string or not is_string(entry, False, True):
        return False
    try:
        entry = str(entry)
        float(entry)
        return True
    except:
        return False


def is_int(entry: Any, check_string: bool = False) -> TypeGuard[int]:
    """Checks if a number is a valid integer.

    Args:
        entry (Any): The item to be check if is a valid integer
        check_string (bool, optional): To check strings to see if its a possible number. Defaults to False.

    Returns:
        bool: True if its a True integer otherwise False.
    """
    if isinstance(entry, int):
        return True
    if not check_string or not is_string(entry, False, True):
        return False
    return str(entry).isdigit()


def is_dict(entry: Any, allow_empty: bool = False) -> TypeGuard[dict]:
    """Check if the provided entry is a valid dictionary and if it has content or not (if allow_empty is False).

    Args:
        entry (Any): The value to be checked if its True.
        allow_empty (bool, optional): If True it allow empty dictionaries to be evaluated, otherwise it requires it to be a dictionary and have at least some content there. Defaults to False.

    Returns:
        bool: True if valid dictionary and (if allow_empty is False) if it has some content in it.
    """
    return isinstance(entry, dict) and (allow_empty or bool(entry))


def is_number(entry: Any, check_string: bool = False) -> TypeGuard[Union[int, float]]:
    """Check if the entry is a number (being either a int or float). It also check if in case its a string (and check_string is True) if its a valid number if converted.

    Args:
        entry (Any): The entry to be checked.
        check_string (bool, optional): If True will check if entry can be converted to float, case the entry is a string. Defaults to False.

    Returns:
        bool: True if the entry is either a float or a integer, otherwise False.

    Examples:
        if for example 'entry' is a string and check_string is set to True:
        ```python
        a = "1"
        b = "text"
        c = "1.56"
        print(is_number(a, check_string=True)) # True
        print(is_number(a, check_string=False)) # False
        print(is_number(b, check_string=True)) # False
        print(is_number(b, check_string=False)) # False
        print(is_number(c, check_string=True)) # True
        print(is_number(c, check_string=False)) # False
        float(a) # ok
        float(b) # ValueError
        float(c) # ok
        ```

    """
    return is_int(entry, check_string) or is_float(entry, check_string)


def is_string(
    entry: Any,
    strip_string: bool = True,
    allow_empty: bool = False,
    check_path: bool = True,
) -> TypeGuard[Union[str, bytes]]:
    """Check if an entry is a string, bytes or a Path object.

    if ``strip_string`` is set to True, then the entry will be striped will be stripped before the final checking (Its useless when allow empty is False).
    """

    if not isinstance(entry, (str, bytes)):
        if not check_path or not isinstance(entry, Path):
            return False
    if isinstance(entry, Path):
        entry = str(entry)
    if not allow_empty and strip_string:
        entry = entry.strip()
    return allow_empty or bool(entry)


def validate_path(
    entry: Any,
    only_check_types: bool = False,
    *,
    allow_empty: bool = True,
    do_validate_path: bool = False,
    path_type: Literal["file", "dir", "all"] = "all",
) -> TypeGuard[Union[str, bytes, Path]]:
    """Check if an entry is valid path object. Optionally checks if the path is also valid or not.

    Args:
        entry (Any): The patch to be verified.

        only_check_types (bool, optional): If set to True, it will skip all the other steps, and just check
                                           if the type is a str, bytes or Path object. Defaults to False.

        allow_empty (bool, optional): If the entry is an empty string or Path, and this value is set to True
                                    the results will be True when the ``path_type`` is "dir"
                                    otherwise it will return False. Defaults to True.

        do_validate_path (bool, optional): If set to True it will raises an assertion error when either,
                                        the path does not exist, or if it is empty and ``allow_empty``
                                        is set to false, or the path is not the correct ``path_type``. Defaults to False.

        path_type (Literal["file", "dir", "all"], optional): Selects the type of path to be checked.
                                                            If set to:
                                                            - "all": returns True if Path exists.
                                                            - "file": returns True if Path exists and is a file.
                                                            - "dir": returns True if Path exists and is a directory (not a file).
                                                            Defaults to "all".

    Returns:
        TypeGuard[Union[str, bytes, Path]]: If True, then the path is considered valid for your objectives.
    """
    entry_type = isinstance(entry, (str, bytes, Path))
    if only_check_types:
        # we only do the assertion as usual.
        assert (
            not do_validate_path or entry_type
        ), f"Invalid Path type! '{type(entry) }' is not considered a valid path object."
        return entry_type

    assert path_type in [
        "file",
        "dir",
        "all",
    ], f'Invalid path_type ({path_type}) It needs to be either "file", "dir" or "all"'

    if not entry_type:
        assert (
            not do_validate_path
        ), f"Invalid Path type! '{type(entry) }' is not considered a valid path object."
        return False

    entry = str(entry).strip()
    if not entry:
        validation = allow_empty and path_type == "dir"
        assert not do_validate_path or validation, "Empty path is not allowed!"
        return validation

    # Converts back to path
    entry: Path = Path(entry)

    if not entry.exists():
        assert not do_validate_path, f"Invalid Path! '{entry}' does not exist!"
        return False

    if path_type == "all":
        # Since we already verified above, this is already confirmed.
        return True

    elif path_type == "file":
        validation = entry.is_file()
        assert not do_validate_path or validation, f"'{entry}' Is not a valid file."
        return validation

    validation = entry.is_dir()
    assert not do_validate_path or validation, f"'{entry}' Is not a valid directory."
    return validation


def is_path(
    entry: Any,
    only_check_types: bool = False,
    *,
    allow_empty: bool = True,
    do_validate_path: bool = False,
    path_type: Literal["file", "dir", "all"] = "all",
) -> TypeGuard[Path]:
    """Similar to ``validate_path`` but will only return True if the entry is a ``Path`` object (pathlib's Path).

    Check if an entry is valid path object. Optionally checks if the path is also valid or not.

    Args:
        entry (Any): The patch to be verified.

        only_check_types (bool, optional): If set to True, it will skip all the other steps, and just check
                                           if the type is a str, bytes or Path object. Defaults to False.

        allow_empty (bool, optional): If the entry is an empty string or Path, and this value is set to True
                                    the results will be True when the ``path_type`` is "dir"
                                    otherwise it will return False. Defaults to True.

        do_validate_path (bool, optional): If set to True it will raises an assertion error when either,
                                        the path does not exist, or if it is empty and ``allow_empty``
                                        is set to false, or the path is not the correct ``path_type``. Defaults to False.

        path_type (Literal["file", "dir", "all"], optional): Selects the type of path to be checked.
                                                            If set to:
                                                            - "all": returns True if Path exists.
                                                            - "file": returns True if Path exists and is a file.
                                                            - "dir": returns True if Path exists and is a directory (not a file).
                                                            Defaults to "all".

    Returns:
        TypeGuard[Union[str, bytes, Path]]: If True, then the path is considered valid for your objectives.
    """
    initial_validation = isinstance(entry, Path)
    assert (
        initial_validation or not do_validate_path
    ), f"Invalid typing '{type(entry)}'! It must be a 'Path' type object"
    if only_check_types:
        return initial_validation
    return validate_path(
        entry,
        False,
        allow_empty=allow_empty,
        do_validate_path=do_validate_path,
        path_type=path_type,
    )


def is_list(entry: Any, allow_empty: bool = False) -> TypeGuard[list]:
    """Check if the provided entry is a list and if its not empty.

    Args:
        entry (Any): _description_
        allow_empty (bool, optional): If true, will return True if the item is a list, regardless if its empty or not. Defaults to False.

    Returns:
        bool: True if the entry is a list and if either the allow_empty is true or the list is not empty.
    """
    return isinstance(entry, list) and (allow_empty or bool(entry))


def is_tuple(entry: Any, allow_empty: bool = False) -> TypeGuard[tuple]:
    """Check if the provided entry is a valid dictionary and if it has content or not (if allow_empty is False).

    Args:
        entry (Any): The value to be checked if its True.
        allow_empty (bool, optional): If True it allow empty dictionaries to be evaluated, otherwise it requires it to be a dictionary and have at least some content there. Defaults to False.

    Returns:
        bool: True if valid dictionary and (if allow_empty is False) if it has some content in it.
    """
    return isinstance(entry, tuple) and (allow_empty or bool(entry))


def is_array(
    entry: Any, allow_empty: bool = False, **kwargs
) -> TypeGuard[Union[list, tuple, set]]:
    """Checks if the entry is either a list, tuple or set. It can also check for dictionaries if ``check_dict`` is True. Checks if its empty if allow_empty is False.

    Args:
        entry (Any): Value to be analyzed.
        allow_empty (bool, optional): If True will allow empty arrays to be returned as True. Defaults to False.
    Returns:
        bool: If True the value is a valid (non-empty if allow_empty is False else it returns true just for being a list or tuple).
    """
    if isinstance(entry, (list, tuple, set)):
        return allow_empty or bool(entry)
    return False


def is_bool(entry: Any, allow_number: bool = False) -> TypeGuard[bool]:
    if not allow_number or isinstance(entry, bool):
        return isinstance(entry, bool)
    return is_int(entry) and entry in [0, 1]


def default(entry: Optional[T], default: T) -> T:
    """
    entry if its not None or default.

    Useful to allow a different approach than 'or' operator in strings, for example:

    Consider that the arguments as:
    ```py
    arg1 = 0
    arg2 = 3
    ```
    If using or operator directly the following would happen:

    ```python
    results = arg1 or arg2
    # results = arg2 (3)
    ```
    It checks for Falsely data in the first item, but sometimes that value would be valid even if falsely like: `0`, `""`, `[]`, `{}`, `()` and `False`.

    So, it was made to check if the first value is None or non-None if None it uses the arg2, otherwise it returns the arg1 even if falsely.

    example:
    ```
    from gr1336_toolbox import default

    results_default = default(0, 3)
    # results_default = 0
    results_on_or = 0 or 3
    # results_on_or = 3
    results_default_2 = default(None, 0)
    # results_default_2 = 0
    ```

    """
    return entry if exists(entry) else default


def exists(val: Optional[T]) -> TypeGuard[T]:
    return val is not None


__all__ = [
    "is_int",
    "is_string",
    "is_dict",
    "is_float",
    "is_number",
    "is_tuple",
    "is_list",
    "is_bool",
    "is_array",
    "is_numpy",
    "is_tensor",
    "is_path",
    "exists",
    "default",
]
