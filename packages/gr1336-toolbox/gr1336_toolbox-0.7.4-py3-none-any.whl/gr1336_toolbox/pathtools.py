from pathlib import Path
from typing import Any, Literal, Optional, Union, Sequence, List, Tuple, Dict, TypeGuard
from .types import validate_path, is_string, is_path, is_list, is_array


def _get_files_ext_set(extension: str):
    if extension.startswith("*."):
        return extension
    if extension.startswith("."):
        return "*" + extension
    return "*." + extension


def find(
    path: Union[str, Path],
    path_type: Literal["file", "dir", "all"] = "all",
    *,
    pattern: Optional[str] = None,
) -> list[Path]:
    path = Path(path)
    if not is_string(pattern):
        pattern = "*"
    return [
        x for x in Path(path).glob(pattern) if validate_path(x, path_type=path_type)
    ]


def to_string(path: Path):
    assert isinstance(path, (Path, str, bytes)), "Invalid Path format"
    return str(Path(path)).replace("\\", "/")


def get_name(path: Union[str, Path, bytes]):
    assert isinstance(path, (Path, str, bytes)), "Invalid Path format"
    name = Path(path).name
    if not "." in name:
        return name
    return name[: name.rfind(".")]


def find_dirs(
    path: Union[str, Path],
    pattern: str = "*",
    sort_findings: bool = True,
    *args,
    **kwargs,
) -> list[Path] | list:
    if isinstance(path, list):
        results = []
        paths = [x for x in path if is_path(x, path_type="dir")]
        if not paths:
            return []
        [results.extend(find(x, pattern=pattern, path_type="dir")) for x in paths]
        if sort_findings:
            return sorted(results)
        return results
    if not validate_path(path, path_type="dir"):
        return []
    found = find(path, pattern=pattern, path_type="dir")
    if sort_findings:
        return sorted(found)
    return found


def find_files(
    path: Union[List[Union[str, Path]], str, Path],
    extensions: Optional[Union[str, Sequence[str]]] = None,
):
    results = []
    if is_list(path):
        paths = [Path(x) for x in path if validate_path(x, path_type="path")]
        if not paths:
            return results
        [results.extend(find_files(_path, extensions=extensions)) for _path in paths]
        return list(sorted(results))
    else:
        if not validate_path(path, path_type="dir"):
            return results
        if is_string(extensions):
            extensions = [extensions]

        if is_array(extensions):
            [
                results.extend(
                    find(
                        path,
                        path_type="file",
                        pattern=_get_files_ext_set(extension),
                    )
                )
                for extension in extensions
            ]
        else:
            results.extend(
                find(
                    path,
                    path_type="file",
                )
            )
        return list(sorted(results))


def mkdir(
    *paths: Union[Path, str],
):
    Path(*[x for x in paths if isinstance(x, (bytes, str, Path))]).mkdir(
        parents=True, exist_ok=True
    )


def setup_path(
    *paths: Union[str, Path],
    mkdir_path: bool = False,
    return_original: bool = False,
    **kwargs,
) -> Union[str, Path]:
    """
    The function `setup_path` takes in multiple paths as arguments, creates directories if specified,
    and returns the path as a string with forward slashes.

    Args:
      paths (str | Path): The paths that are to be managed.
      mkdir_path (bool): Create the directory specified in the path if it does not already exist. If `mkdir_path` is set to `True` and the directory does not exist, the function will create the directory. Defaults to False
      return_original (bool): Determines whether the function should return the type of the path (as a `Path` object) instead of the path as a string. If `return_original` is set to `True`, the function. Defaults to False

    Returns:
      The function `setup_path` returns a string representation of the path with backslashes replaced by forward slashes or as a `Path` object if `return_original` is set to True.
    """
    path = Path(*[x for x in paths if isinstance(x, (bytes, str, Path))])
    if mkdir_path and not path.exists():
        mkdir(m_path=path.parent if "." in path.name else path)
    if return_original:
        return path
    return to_string(path)
