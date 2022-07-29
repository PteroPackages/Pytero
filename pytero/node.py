from .servers import AppServer
from .types import Allocation, Location, NodeConfiguration
from .util import transform


__all__ = ('Node')


class Node:
    def __init__(self, http, data: dict[str,]) -> None:
        self._http = http
        self.id: int = data['id']
        self.created_at: str = data['created_at']
        self._patch(data)
        self._patch_relations(data.get('relationships'))
    
    def __repr__(self) -> str:
        return '<Node id=%d>' % self.id
    
    def __str__(self) -> str:
        return self.name
    
    def _patch(self, data: dict[str,]) -> None:
        self.name: str = data['name']
        self.description: str | None = data.get('description')
        self.location_id: int = data['location_id']
        self.location: Location | None = None
        self.allocations: list[Allocation] | None = None
        self.servers: list[AppServer] | None = None
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
        self.updated_at: str | None = data.get('updated_at')
    
    def _patch_relations(self, data: dict[str,] | None) -> None:
        if data is None:
            return
        
        if 'allocations' in data:
            self.allocations = []
            for datum in data['allocations']['data']:
                self.allocations.append(Allocation(**datum['attributes']))
        
        if 'location' in data:
            self.location = Location(**data['location']['attributes'])
        
        if 'servers' in data:
            self.servers = []
            for datum in data['servers']['data']:
                self.servers.append(AppServer(self._http, datum['attributes']))
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'])
    
    async def get_configuration(self) -> NodeConfiguration:
        return await self._http.get_node_configuration(self.id)
    
    def update_node(self) -> None:
        return NotImplemented
