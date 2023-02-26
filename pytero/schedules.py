from typing import Any
from .types import _Http, Cron, Task

# pylint: disable=C0103

__all__ = ('Schedule',)


class Schedule:
    def __init__(self, http: _Http, identifier: str,
                 data: dict[str, Any]) -> None:
        self._http = http
        self.identifier = identifier
        self.tasks: list[Task] = []
        self.id: int = data['id']
        self.name: str = data['name']
        self.cron: Cron = Cron(**data['cron'])
        self.is_active: bool = data['is_active']
        self.is_processing: bool = data['is_processing']
        self.only_when_online: bool = data['only_when_online']
        self.created_at: str = data['created_at']
        self.updated_at: str | None = data.get('updated_at')
        self.last_run_at: str | None = data.get('last_run_at')
        self.next_run_at: str | None = data.get('next_run_at')

    def __repr__(self) -> str:
        return f'<Schedule id={self.id} name={self.name} \
            tasks={len(self.tasks)}>'

    def __str__(self) -> str:
        return self.name
