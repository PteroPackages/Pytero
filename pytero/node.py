from typing import Optional
from .types import NodeConfiguration
from .util import transform


__all__ = ('Node')

class Node:
    def __init__(self, http, data: dict[str,]) -> None:
        self._http = http
        self.id: int = data['id']
        self.created_at: str = data['created_at']
        self._patch(data)
    
    def __repr__(self) -> str:
        return '<Node id=%d>' % self.id
    
    def __str__(self) -> str:
        return self.name
    
    def _patch(self, data: dict[str,]) -> None:
        self.name: str = data['name']
        self.description: Optional[str] = data.get('description')
        self.location_id: int = data['location_id']
        self.public: bool = data['public']
        self.fqdn: str = data['fqdn']
        self.scheme: str = data['scheme']
        self.behind_proxy: bool = data['behind_proxy']
        self.memory: int = data['memory']
        self.memory_overallocate: int = data['memory_overallocate']
        self.disk: int = data['disk']
        self.disk_overallocate: int = data['disk_overallocate']
        self.daemon_base: str = data['daemon_base']
        self.daemon_sftp: int = data['daemon_sftp']
        self.daemon_listen: int = data['daemon_listen']
        self.maintenance_mode: bool = data['maintenance_mode']
        self.upload_size: int = data['upload_size']
        self.updated_at: Optional[str] = data.get('updated_at')
    
    def _patch_relations(self) -> None:
        pass
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'])
    
    async def get_configuration(self) -> NodeConfiguration:
        return await self._http.get_node_configuration(self.id)
    
    def update_node(self) -> None:
        return NotImplemented
