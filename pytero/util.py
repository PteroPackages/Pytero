from typing import Any, Callable


__all__ = ('transform')

def transform(
    data: object,
    *,
    ignore: list[str] = [],
    cast: dict[str, Callable[..., Any]] = {},
    maps: dict[str, str] = {}
) -> dict[str,]:
    res = {}
    
    for key, value in data.__dict__.items():
        if key in ignore:
            continue
        
        if maps.get(key):
            key = maps[key]
        
        if key in cast:
            try:
                res[key] = cast[key](value)
            except:
                res[key] = str(value)
        else:
            if hasattr(value, 'to_dict'):
                res[key] = value.to_dict()
            else:
                res[key] = value
    
    return res
