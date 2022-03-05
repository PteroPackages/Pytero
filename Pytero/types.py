from dataclasses import dataclass
from typing import Callable


class _RequestManager:
    ping: float
    get_headers: Callable[[], dict[str, str]]
    _make: Callable[[str, str, dict | None], dict[str,] | None]
    rget: Callable[[str], dict[str,] | None]
    rpost: Callable[[str, dict | None], dict[str,] | None]
    rpatch: Callable[[str, dict | None], dict[str,] | None]
    rput: Callable[[str, dict | None], dict[str,] | None]
    rdelete: Callable[[str], dict[str,] | None]
    on_receive: Callable[[dict[str,]], None]
    on_debug: Callable[[str], None]


class _PteroApp:
    domain: str
    auth: str
    options: None
    requests: _RequestManager


@dataclass
class Nest:
    id: int
    uuid: str
    author: str
    name: str
    description: str
    created_at: str
    updated_at: str | None

    def __repr__(self) -> str:
        return '<Nest id=%d name=%s>' % (self.id, self.name)


@dataclass
class NodeConfiguration:
    debug: bool
    uuid: str
    token_id: str
    token: str
    api: dict[str, int | str | dict[str, str | bool]]
    system: dict[str, str | dict[str, int]]
    allowed_mounts: list[str]
    remote: str


@dataclass
class NodeLocation:
    id: int
    long: str
    short: str
    created_at: str
    updated_at: str | None

    def __repr__(self) -> str:
        return '<NodeLocation id=%d long=%s short=%s>' \
            % (self.id, self.long, self.short)
