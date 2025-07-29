import os
import json
import yaml
import shutil
import traceback
from pathlib import Path
from .text import current_time
from .types import is_string, is_array, is_list, is_dict, validate_path
from typing import Any, Literal, Optional, Union, Sequence, List, Tuple, Dict
from .misc import flatten_list, filter_list
from .pathtools import *


def load_json(
    path: Union[str, Path],
    default_value: Optional[Any] = None,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    *args,
    **kwargs,
) -> list | dict | None:
    """
    Load JSON/JSONL data from a file.

    Args:
        path (Union[str, Path]): The path to the JSON file.

    Returns:
        Union[list, dict, None]: The loaded JSON data as a list, dictionary, or None if any error occurs.
    """

    if not validate_path(path, path_type="file"):
        if default_value is None:
            raise FileNotFoundError(f"Invalid path '{path}'")
        return default_value
    path = Path(path)
    file = path.read_text(encoding=encoding, errors=errors)
    if path.name.endswith(".jsonl"):
        results = []
        for line in file.splitlines():
            try:
                results.append(json.loads(line))
            except Exception as e:
                pass
        return results
    try:
        return json.loads(file)
    except:
        return default_value


def save_json(
    path: Union[str, Path],
    content: Union[list, dict, tuple, map, str, bytes],
    indent: int = 4,
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    separators: tuple[str, str] | None = None,
    sort_keys: bool = False,
    **kwargs,
) -> None:
    """
    Save JSON data to a file.

    Args:
        path (Union[str, Path]): The path to save the JSON file.
        content (Union[list, dict]): The content to be saved as JSON.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".
        indent (int, optional): The indentation level in the saved JSON file. Defaults to 4.
    """

    if not is_string(path):
        path = current_time() + ".json"
    path = Path(path)
    if not path.name.endswith((".json", ".jsonl")):
        path = Path(path.parent, f"{path.name}.json")
    mkdir(Path(path).parent)

    dumps_kwargs = dict(
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        separators=separators,
        sort_keys=sort_keys,
    )
    if path.name.endswith(".jsonl"):
        append_content = ""
        if path.exists():
            append_content = (
                path.read_text(encoding=encoding, errors=errors).rstrip() + "\n"
            )
        if is_string(content, True):
            content = content.rstrip()
        else:
            content = json.dumps(content, **dumps_kwargs).rstrip()
        content = append_content.rstrip() + content
    else:
        content = json.dumps(content, indent=indent, **dumps_kwargs)
    path.write_text(content, encoding=encoding, errors=errors)


def load_text(
    path: Union[Path, str],
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    default_value: Optional[Any] = None,
    returns_default_on_fail: bool = False,
    **kwargs,
) -> str:
    if not validate_path(path, path_type="file"):
        if default_value is None and not returns_default_on_fail:
            raise FileNotFoundError(f"Invalid path '{path}'")
        return default_value
    try:
        return Path(path).read_text(encoding, errors=errors)
    except Exception as e:
        print(f"Exception: {e}")
        if returns_default_on_fail:
            traceback.print_exc()
            return default_value
        else:
            raise e


def save_text(
    path: Union[Path, str],
    content: str,
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    newline: Optional[str] = None,
    raises: bool = True,
    **kwargs,
) -> None:
    """Save a text file to the provided path.

    args:
        raises: (bool, optional): If False, it will not raise the exception when somehting goes wrong, instead it will just print the traceback.
    """
    try:
        path = Path(path)
        mkdir(Path(path).parent)
        path.write_text(content, encoding=encoding, errors=errors, newline=newline)
    except Exception as e:
        print(f'save_text: Error on saving "{path}". Exception: {e}')
        if raises:
            raise e
        else:
            traceback.print_exc()


def load_yaml(
    path: Union[Path, str],
    *,
    default_value: Any | None = None,
    safe_loader: bool = False,
    returns_default_on_fail: bool = False,
    **kwargs,
) -> Optional[Union[List[Any], Dict[str, Any]]]:
    """
    Loads YAML content from a file.

    Args:
        path (Union[Path, str]): The path to the file.
        default_value (Any | None): If something goes wrong, this value will be returned instead.
        safe_loader (bool): If True, it will use the safe_load instead.
        returns_default_on_fail (bool): If True, when a exception occurs on the file loading it will returns the default value.
                                        this affects both if the file does not pass the validation, even without a default value being set or an exception is raisen by the loader.

    Returns:
        Optional[Union[List[Any], Dict[str, Any]]]: The loaded YAML data.
    """
    if not validate_path(path, path_type="file"):
        if default_value is None and not returns_default_on_fail:
            raise FileNotFoundError(f"Invalid path '{path}'")
        return default_value
    loader = yaml.safe_load if safe_loader else yaml.unsafe_load
    try:
        return loader(Path(path).read_bytes())
    except Exception as e:
        print(f"YAML load error: {e}")
        print("----------------------")
        if not returns_default_on_fail:
            raise e
        traceback.print_exc()
        return default_value


def save_yaml(
    path: Union[Path, str],
    content: Union[List[Any], Tuple[Any, Any], Dict[Any, Any]],
    *,
    encoding: Optional[
        Union[str, Literal["utf-8", "ascii", "unicode-escape", "latin-1"]]
    ] = None,
    errors: Union[str, Literal["strict", "ignore"]] = "strict",
    safe_dump: bool = False,
    raises: bool = True,
    **kwargs,
) -> None:
    """Saves a YAML file to the provided path.

    Args:
        path (Union[Path, str]): The path where the file will be saved.
        content (Union[List[Any], Tuple[Any, Any], Dict[Any, Any]]): The data that will be written into the file.
        encoding (str, optional): The encoding of the output. Default is 'utf-8'. Defaults to "utf-8".
        safe_dump (bool, optional): If True, it uses the safe_dump method instead. Defaults to False.
        raises: (bool, optional): If False, it will not raise the exception when somehting goes wrong, instead it will just print the traceback.
    """
    mkdir(Path(path).parent)
    save_func = yaml.safe_dump if safe_dump else yaml.dump
    try:
        with open(path, "w", encoding=encoding, errors=errors) as file:
            save_func(data=content, stream=file, encoding=encoding)
    except Exception as e:
        print(f'save_yaml: Error on saving "{path}". Exception: {e}')
        if raises:
            raise e
        else:
            traceback.print_exc()


def move(
    source: Union[str, Path],
    destination: Union[str, Path],
    *args,
    **kwargs,
):
    """
    Moves a file or directory from one location to another.

    Args:
        source_path (Union[str, Path]): The path of the file/directory to be moved.
        destination_path (Union[str, Path]): The new location for the file/directory.

    Raises:
        AssertionError: If the source path does not exist or is invalid
    """
    assert str(source).strip() and Path(source).exists(), "Source path does not exists!"
    source = Path(source)
    assert validate_path(source), "Source path does not exists!"
    mkdir(destination)
    shutil.move(str(source), str(destination))


def delete(
    files: Union[str, Path, Sequence[Union[str, Path]]],
    verbose: bool = False,
    *args,
    **kwargs,
):
    if is_string(files) and Path(files).exists():
        files = Path(files)
        if files.is_dir():
            shutil.rmtree(str(files))
        else:
            os.rmdir(str(files))
        if verbose:
            files = to_string(files)
            print(f"'{files}' deleted")
    elif is_array(files):
        [delete(path) for path in filter_list(flatten_list(files), (str, Path))]
