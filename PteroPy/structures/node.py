from typing import Optional


class Node:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.public: bool = data['public']
        self.name: str = data['name'] or self.name
        self.description: Optional[str] = data['description']
        self.location_id: int = data['location_id']
        self.fqdn: str = data['fqdn']
        self.scheme: str = data['scheme']
        self.behind_proxy: bool = data['behind_proxy']
        self.maintenance_mode: bool = data['maintenance_mode']
        self.memory: float = float(data['memory'])
        self.memory_overallocate: float(data['memory_overallocate'])
        self.disk: float = float(data['disk'])
        self.disk_overallocate: float = float(data['disk_overallocate'])
        self.upload_size: int = data['upload_size']
        self.daemon_listen: int = data['daemon_listen']
        self.daemon_sftp: int = data['daemon_sftp']
        self.daemon_base: int = data['daemon_base']
    
    def __repr__(self) -> str:
        return '<Node %d>' % self.id
    
    def __dict__(self) -> dict:
        return { k: getattr(self, k) for k in dir(self) if not k.startswith('_') }
    
    async def getconfig(self):
        return NotImplemented
    
    async def update(self, **kwargs):
        return NotImplemented
    
    async def delete(self):
        return NotImplemented
