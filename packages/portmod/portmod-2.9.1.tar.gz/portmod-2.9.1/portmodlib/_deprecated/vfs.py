# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Functions for interacting with the OpenMW VFS
"""

import os
import shutil
from functools import wraps
from tempfile import gettempdir
from typing import Any, Callable, Dict, List, TypeVar, cast

from portmodlib.archives import extract_archive_file, list_archive
from portmodlib.fs import ci_exists, is_parent
from portmodlib.functools import prefix_aware_cache
from portmodlib.globals import root
from portmodlib.l10n import l10n
from portmodlib.parsers.list import read_list

F = TypeVar("F", bound=Callable[..., Any])
_VFS_CACHE_FUNCS = []


def vfs_cache(func: F) -> F:
    """
    A variant of functools.lru_cache which treats the prefix as if it were an argument
    """

    @wraps(func)
    @prefix_aware_cache
    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    _VFS_CACHE_FUNCS.append(inner)

    return cast(F, inner)


def clear_vfs_cache():
    for func in _VFS_CACHE_FUNCS:
        func.cache_clear()  # type: ignore


@vfs_cache
def find_file(name: str) -> str:
    """
    Locates the path of a file within the OpenMW virtual file system

    .. deprecated:: 2.4
        It will be removed in Portmod 3.0

    args:
        name: The relative path within the VFS to search for

    returns:
        The absolute path of the file
    """
    # FIXME: This should respect the CASE_INSENSITIVE_FILES setting
    if os.environ.get("VFS"):
        for directory in reversed(get_vfs_dirs()):
            path = ci_exists(os.path.join(directory, name))
            if path:
                return path

        for archive in reversed(get_vfs_archives()):
            contents = list_archive(archive)
            for file in contents:
                if os.path.normpath(file).lower() == os.path.normpath(name).lower():
                    return extract_archive_file_to_tmp(archive, file)
    else:
        path = ci_exists(name, prefix=root())
        if path:
            return path

    raise FileNotFoundError(name)


@vfs_cache
def list_dir(name: str) -> List[str]:
    """
    Locates all path of files matching the given pattern within the OpenMW
    virtual file system

    .. deprecated:: 2.4
        It will be removed in Portmod 3.0

    args:
        name: The relative path of the directory within the VFS
    returns:
        A list of files contained within the directory
    """
    files: Dict[str, str] = {}
    normalized = os.path.normpath(name).lower()

    # FIXME: This should respect the CASE_INSENSITIVE_FILES setting

    if os.environ.get("VFS"):
        for directory in reversed(get_vfs_dirs()):
            path = ci_exists(os.path.join(directory, normalized))
            if path:
                for file in os.listdir(path):
                    if file.lower() not in files:
                        files[file.lower()] = file

        for archive in reversed(get_vfs_archives()):
            contents = list_archive(archive)
            for file in contents:
                if is_parent(os.path.normpath(file).lower(), normalized):
                    suffix = os.path.relpath(os.path.normpath(file).lower(), normalized)
                    component, _, _ = suffix.partition(os.sep)
                    files[component] = component
    else:
        path = ci_exists(normalized, prefix=root())
        if path:
            for file in os.listdir(path):
                if file.lower() not in files:
                    files[file.lower()] = file

    return sorted(files.values())


def _cleanup_tmp_archive_dir():
    path = os.path.join(gettempdir(), ".archive_files")
    if os.path.exists(path):
        shutil.rmtree(path)


def extract_archive_file_to_tmp(archive: str, file: str) -> str:
    """Extracts the given file from the archive and places it in a temprorary directory"""
    temp = gettempdir()
    output_dir = os.path.join(
        temp, ".archive_files", os.path.basename(archive), os.path.dirname(file)
    )
    os.makedirs(output_dir, exist_ok=True)
    result_file = os.path.join(output_dir, os.path.basename(file))
    extract_archive_file(archive, file, output_dir)
    if not os.path.exists(result_file):
        raise Exception(l10n("archive-extraction-failed", file=file, dest=result_file))
    return result_file


@vfs_cache
def get_vfs_dirs() -> List[str]:
    """Returns an ordered list of the VFS directories, in reverse order of priority"""
    dirs: List[str] = read_list(
        os.path.join(root(), os.environ["VARIABLE_DATA"], "vfs")
    )
    return dirs


@vfs_cache
def get_vfs_archives() -> List[str]:
    """Returns an ordered list of the VFS directories, in reverse order of priority"""
    archives: List[str] = read_list(
        os.path.join(root(), os.environ["VARIABLE_DATA"], "vfs-archives")
    )
    return archives
