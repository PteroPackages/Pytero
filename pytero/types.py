"""General data, enum and typing classes for Pytero."""

from dataclasses import dataclass
from typing import Any, Callable, Optional

# pylint: disable=C0103

__all__ = (
    '_Http',
    'Activity',
    'Allocation',
    'APIKey',
    'AppDatabase',
    'ClientDatabase',
    'ClientHost',
    'ClientVariable',
    'Container',
    'Cron',
    'DeployNodeOptions',
    'DeployServerOptions',
    'EggScript',
    'EggConfiguration',
    'EggRelashionships',
    'Egg',
    'FeatureLimits',
    'Limits',
    'Location',
    'Nest',
    'NetworkAllocation',
    'NodeConfiguration',
    'Resources',
    'SSHKey',
    'Statistics',
    'Task',
    'WebSocketAuth',
    'WebSocketEvent',
    'Backup'
)


class _Http:
    url: str
    key: str
    _raw: Callable[[str, str, Any | None], Any]
    get: Callable[[str], Any]
    post: Callable[[str], Any]
    patch: Callable[[str], Any]
    put: Callable[[str], Any]
    delete: Callable[[str], Any]


@dataclass
class Activity:
    id: str
    batch: str
    event: str
    is_api: bool
    ip: Optional[str]
    description: Optional[str]
    properties: dict[str, Any]
    has_additional_metadata: bool
    timestamp: str

    def __repr__(self) -> str:
        return f'<Activity event={self.event}>'

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Allocation:
    id: int
    ip: str
    alias: str | None
    port: int
    notes: str | None
    assigned: bool

    def __repr__(self) -> str:
        return f'<Allocation id={self.id} ip={self.ip} port={self.port}>'

    def to_dict(self) -> dict[str, Any]:
        d = self.__dict__
        del d['id']
        return d


@dataclass
class APIKey:
    identifier: str
    description: str
    allowed_ips: list[str]
    created_at: str
    last_used_at: Optional[str]

    def __repr__(self) -> str:
        return f'<APIKey identifier={self.identifier}>'


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
    password: str | None = None


@dataclass
class ClientHost:
    address: str
    port: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class ClientDatabase:
    id: str
    name: str
    username: str
    host: ClientHost
    connections_from: str
    max_connections: int

    def to_dict(self) -> dict[str, Any]:
        d = self.__dict__
        del d['id']
        return d


@dataclass
class ClientVariable:
    name: str
    description: str
    env_variable: str
    default_value: str | None
    server_value: str | None
    is_editable: bool
    rules: str


@dataclass
class Container:
    startup_command: str
    environment: dict[str, int | str | bool]
    image: str
    installed: bool

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Cron:
    day_of_week: str
    day_of_month: str
    month: str
    hour: str
    minute: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class DeployServerOptions:
    locations: list[int]
    dedicated_ip: bool
    port_range: list[str]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class DeployNodeOptions:
    memory: int
    disk: int
    location_ids: list[int]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class EggConfiguration:
    files: list[str]
    startup: dict[str, str]
    stop: str
    logs: list[str]
    file_denylist: list[str]
    extends: Optional[str]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class EggScript:
    privileged: bool
    install: str
    entry: str
    container: str
    extends: Optional[str]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class EggRelashionships:
    config: dict
    script: dict
    variables: dict

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


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
    updated_at: Optional[str] = None
    relationships: Optional[dict] = None

    def __repr__(self) -> str:
        return f'<Egg id={self.id} nest=#{self.nest} name={self.name}>'

    def to_dict(self) -> dict[str, Any]:
        d = self.__dict__
        del d['id'], d['uuid'], d['created_at'], d['updated_at']
        return d


@dataclass
class FeatureLimits:
    allocations: int
    backups: int
    databases: int

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class Limits:
    memory: int
    disk: int
    swap: int
    io: int
    cpu: int
    threads: Optional[str]
    oom_disabled: Optional[bool]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


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
        return f'<Nest id={self.id} name={self.name}>'

    def to_dict(self) -> dict[str, Any]:
        return {
            'author': self.author,
            'name': self.name,
            'description': self.description}


@dataclass
class NetworkAllocation:
    id: int
    ip: str
    ip_alias: str | None
    port: int
    notes: str | None
    is_default: bool

    def __repr__(self) -> str:
        return f'<NetworkAllocation id={self.id} ip={self.ip} \
            port={self.port}>'


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
        return f'<NodeConfiguration uuid={self.uuid}>'


@dataclass
class Location:
    id: int
    long: str
    short: str
    created_at: str
    updated_at: str | None

    def __repr__(self) -> str:
        return f'<Location id={self.id} long={self.long} short={self.short}>'


@dataclass
class Resources:
    memory_bytes: int
    cpu_absolute: int
    disk_bytes: int
    network_rx_bytes: int
    network_tx_bytes: int
    uptime: int

    def __repr__(self) -> str:
        return f'<Resources memory={self.memory_bytes} disk={self.disk_bytes} \
            cpu={self.cpu_absolute}>'


@dataclass
class SSHKey:
    name: str
    fingerprint: str
    public_key: str
    created_at: str


@dataclass
class Statistics:
    current_state: str
    is_suspended: bool
    resources: Resources

    def __repr__(self) -> str:
        return f'<Statistics state={self.current_state} \
            suspended={self.is_suspended}>'


@dataclass
class Task:
    id: int
    sequence_id: int
    action: str
    payload: str
    time_offset: int
    is_queued: bool
    continue_on_failure: bool
    created_at: str
    updated_at: str | None


@dataclass
class WebSocketAuth:
    socket: str
    token: str


@dataclass
class WebSocketEvent:
    event: str
    args: list[str] | None


@dataclass
class Backup:
    uuid: str
    is_successful: bool
    is_locked: bool
    name: str
    ignored_files: list[str]
    checksum: str | None
    bytes: int
    created_at: str
    completed_at: str | None

    def __repr__(self) -> str:
        return f'<Backup uuid={self.uuid}>'
