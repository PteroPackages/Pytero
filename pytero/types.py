from dataclasses import dataclass
from typing import Optional


__all__ = (
    'Activity',
    'Allocation',
    'APIKey',
    'AppDatabase',
    'DeployNodeOptions',
    'DeployServerOptions',
    'EggScript',
    'EggConfiguration',
    'Egg',
    'FeatureLimits',
    'Limits',
    'Location',
    'Nest',
    'NodeConfiguration',
    'SSHKey',
    'WebSocketAuth',
    'WebSocketEvent'
)

@dataclass
class Activity:
    batch: str
    event: str
    is_api: bool
    ip: Optional[str]
    description: Optional[str]
    properties: dict[str,]
    has_additional_metadata: bool
    timestamp: str

    def __repr__(self) -> str:
        return '<Activity event=%s>' % self.event


@dataclass
class Allocation:
    id: int
    ip: str
    alias: str | None
    port: int
    notes: str | None
    assigned: bool

    def __repr__(self) -> str:
        return '<Allocation id=%d ip=%s port=%d>' % (self.id, self.ip, self.port)


@dataclass
class APIKey:
    identifier: str
    description: str
    allowed_ips: list[str]
    created_at: str
    last_used_at: Optional[str]

    def __repr__(self) -> str:
        return '<APIKey identifier=%s>' % self.identifier


@dataclass
class AppDatabase:
    id: int
    server: int
    host: int
    database: str
    username: str
    remote: str
    max_connections: str
    created_at: str
    updated_at: Optional[str]


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
class EggConfiguration:
    files: list[str]
    startup: dict[str, str]
    stop: str
    logs: list[str]
    file_denylist: list[str]
    extends: Optional[str]


@dataclass
class EggScript:
    privileged: bool
    install: str
    entry: str
    container: str
    extends: Optional[str]


@dataclass
class Egg:
    id: int
    uuid: str
    name: str
    author: str
    description: str
    nest: int
    # technically deprecated
    docker_image: str
    docker_images: dict[str, str]
    config: EggConfiguration
    startup: str
    script: EggScript
    created_at: str
    updated_at: Optional[str]

    def __repr__(self) -> str:
        return '<Egg id=%d nest=%d name=%s>' % (self.id, self.nest, self.name)


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
class Location:
    id: int
    long: str
    short: str
    created_at: str
    updated_at: str | None

    def __repr__(self) -> str:
        return '<Location id=%d long=%s short=%s>' % (self.id, self.long, self.short)


@dataclass
class SSHKey:
    name: str
    fingerprint: str
    public_key: str
    created_at: str


@dataclass
class WebSocketAuth:
    socket: str
    token: str

@dataclass
class WebSocketEvent:
    event: str
    args: list[str] | None
