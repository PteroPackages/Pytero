'''Utility functions for Pytero.'''

from typing import Any, Callable


__all__ = ('transform',)


def transform(
    data: object,
    *,
    ignore: list[str] = None,
    cast: dict[str, Callable[..., Any]] = None,
    maps: dict[str, str] = None
) -> dict[str, Any]:
    '''Transforms an object into its JSON object form.'''
    res = {}
    if ignore is None:
        ignore = []

    if cast is None:
        cast = {}

    if maps is None:
        maps = {}

    for key, value in data.__dict__.items():
        if key in ignore:
            continue

        if maps.get(key):
            key = maps[key]

        if key in cast:
            try:
                res[key] = cast[key](value)
            except TypeError:
                res[key] = str(value)
        else:
            if hasattr(value, 'to_dict'):
                res[key] = value.to_dict()
            else:
                res[key] = value

    return res
