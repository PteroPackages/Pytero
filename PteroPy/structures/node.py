from typing import Optional


class Node:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.public: Optional[bool] = data.get('public', None)
        self.name: str = data.get('name')
        self.description: Optional[str] = data.get('description', None)
        self.location_id: int = data.get('location_id', -1)
        self.fqdn: str = data.get('fqdn')
        self.scheme: str = data.get('scheme', 'HTTPS')
        self.behind_proxy: bool = data.get('behind_proxy')
        self.maintenance_mode: bool = data.get('maintenance_mode')
        self.memory: int = data.get('memory')
        self.memory_overallocate: int = data.get('memory_overallocate', 0)
        self.disk: int = data.get('disk')
        self.disk_overallocate: int = data.get('disk_overallocate', 0)
        self.upload_size: int = data.get('upload_size', 0)
        self.daemon_listen: str = data.get('daemon_listen')
        self.daemon_sftp: str = data.get('daemon_sftp')
        self.daemon_base: str = data.get('daemon_base')
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return '<Node id=%d name=%s>' % (self.id, self.name)
    
    def getconfig(self):
        return NotImplemented
    
    def update(self, **kwargs):
        return NotImplemented
    
    def delete(self):
        return NotImplemented
