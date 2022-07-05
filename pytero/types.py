from dataclasses import dataclass
from typing import Optional


__all__ = (
    'Allocation',
    'DeployNodeOptions',
    'DeployServerOptions',
    'FeatureLimits',
    'Limits',
    'Nest',
    'NodeConfiguration',
    'NodeLocation'
)

@dataclass
class Allocation:
    id: int
    ip: str
    alias: str | None
    port: int
    notes: str | None
    assigned: bool

    def __repr__(self) -> str:
        return '<Allocation id=%d ip=%s port=%d>' \
            % (self.id, self.ip, self.port)



@dataclass
class Container:
    startup_command: str
    environment: dict[str, int | str | bool]
    image: str
    installed: bool


@dataclass
class DeployServerOptions:
    locations: list[int]
    dedicated_ip: bool
    port_range: list[str]

    def to_dict(self) -> dict[str,]:
        return {
            'locations': self.locations,
            'dedicated_ip': self.dedicated_ip,
            'port_range': self.port_range}


@dataclass
class DeployNodeOptions:
    memory: int
    disk: int
    location_ids: list[int]

    def to_dict(self) -> dict[str,]:
        return {
            'memory': self.memory,
            'disk': self.disk,
            'location_ids': self.location_ids}


@dataclass
class FeatureLimits:
    allocations: int
    backups: int
    databases: int

    def to_dict(self) -> dict[str,]:
        return {
            'allocations': self.allocations,
            'backups': self.backups,
            'databases': self.databases}


@dataclass
class Limits:
    memory: int
    disk: int
    swap: int
    io: int
    cpu: int
    threads: Optional[str]
    oom_disabled: Optional[bool]

    def to_dict(self) -> dict[str,]:
        return {
            'memory': self.memory,
            'disk': self.disk,
            'swap': self.swap,
            'io': self.io,
            'cpu': self.cpu,
            'threads': self.threads,
            'oom_disabled': self.oom_disabled}


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

    def __repr__(self) -> str:
        return '<NodeConfiguration uuid=%s>' % self.uuid


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
