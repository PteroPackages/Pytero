def select(obj: dict, keys: list[str]) -> dict:
    return {k: obj[k] for k in obj if k in keys}


def transform(
    data: object,
    *,
    ignore: list[str] = [],
    cast: dict[str,] = [],
    maps: dict[str, str] = []
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
            res[key] = value
    
    return res
