# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3
"""
Module building on behaviour from the builtin functools  module
"""

from functools import lru_cache, wraps
from typing import Any, Callable, Generic, Hashable, List, Optional, TypeVar, cast

from portmodlib._deprecated.vfs import clear_vfs_cache

from .globals import env

_T = TypeVar("_T")

# Strictly speaking, everything in this list should be a function
# with a method called cache_clear()
# The cache_clear function could be stored directly, making it easier to type
# But mypy still won't recognize that functions produced by @wraps have a cache_clear method
_SYSTEM_CACHE_FUNCS: List[Any] = []
_INSTALL_CACHE_FUNCS: List[Any] = []


class _lru_cache_wrapper(Generic[_T]):
    __wrapped__: Callable[..., _T]

    def __call__(self, *args: Hashable, **kwargs: Hashable) -> _T:  # type: ignore
        ...

    def cache_clear(self) -> None: ...


def system_cache(func: Callable[..., _T]) -> _lru_cache_wrapper[_T]:
    """
    A variant of lru_cache which gets registered so that caches can be cleared more easily

    This should be used for cached functions which are dependent on the host system, and
    may need to be invalidated in long-running processses.
    """

    @wraps(func)
    @lru_cache()
    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    _SYSTEM_CACHE_FUNCS.append(inner)

    return cast(_lru_cache_wrapper[_T], inner)


def prefix_aware_cache(func: Callable[..., _T]) -> _lru_cache_wrapper[_T]:
    """
    A variant of functools.lru_cache which treats the prefix as if it were an argument

    Like system_cache, but for data which is specific to a certain prefix
    """

    @wraps(func)
    @lru_cache(maxsize=None)
    def inner(_prefix: Optional[str], *args, **kwargs):
        return func(*args, **kwargs)

    @wraps(func)
    def prefix_wrapper(*args, **kwargs):
        return inner(env.PREFIX_NAME, *args, **kwargs)

    prefix_wrapper.cache_clear = inner.cache_clear  # type: ignore
    _SYSTEM_CACHE_FUNCS.append(prefix_wrapper)
    return cast(_lru_cache_wrapper[_T], prefix_wrapper)


def install_cache(func: Callable[..., _T]) -> _lru_cache_wrapper[_T]:
    """
    A variant of functools.lru_cache which treats the prefix as if it were an argument

    like prefix_aware_cache, but for data which portmod itself may change when installing
    packages.
    """

    @wraps(func)
    @prefix_aware_cache
    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    _INSTALL_CACHE_FUNCS.append(inner)

    return cast(_lru_cache_wrapper[_T], inner)


def clear_install_cache():
    for func in _INSTALL_CACHE_FUNCS:
        func.cache_clear()
    clear_vfs_cache()


def clear_system_cache():
    for func in _SYSTEM_CACHE_FUNCS:
        func.cache_clear()
    clear_vfs_cache()
