from typing import Optional
from ..types import _PteroApp


class Node:
    def __init__(self, client: _PteroApp, data: dict[str,]) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self._patch(data)
    
    def _patch(self, data: dict[str,]) -> None:
        self.public: bool = data['public']
        self.name: str = data['name'] or self.name
        self.description: Optional[str] = data['description'] or None
        self.location_id: int = data['location_id']
        self.fqdn: str = data['fqdn']
        self.scheme: str = data['scheme']
        self.behind_proxy: bool = data['behind_proxy']
        self.maintenance_mode: bool = data['maintenance_mode']
        self.memory: int = data['memory']
        self.memory_overallocate: int = data['memory_overallocate']
        self.disk: int = data['disk']
        self.disk_overallocate: int = data['disk_overallocate']
        self.upload_size: int = data['upload_size']
        self.daemon_listen: int = data['daemon_listen']
        self.daemon_sftp: int = data['daemon_sftp']
        self.daemon_base: int = data['daemon_base']
    
    def __repr__(self) -> str:
        return '<Node id=%d>' % self.id
    
    async def getconfig(self):
        return NotImplemented
    
    async def update(self, **kwargs):
        return NotImplemented
    
    async def delete(self):
        return NotImplemented
