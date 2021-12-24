from typing import Optional


class Node:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.public: bool
        self.name: str
        self.description: Optional[str]
        self.location_id: int
        self.fqdn: str
        self.scheme: str
        self.behind_proxy: bool
        self.maintenance_mode: bool
        self.memory: float
        self.memory_overallocate: float
        self.disk: float
        self.disk_overallocate: float
        self.upload_size: int
        self.daemon_listen: int
        self.daemon_sftp: int
        self.daemon_base: int
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        # (setattr(self, k, data[k]) for k in data.keys())
        
        self.public = data.get('public', self.public)
        self.name = data.get('name', self.name)
        self.description = data.get('description', self.description)
        self.location_id = data.get('location_id', self.location_id)
        self.fqdn = data.get('fqdn', self.fqdn)
        self.scheme = data.get('scheme', self.scheme)
        self.behind_proxy = data.get('behind_proxy', self.behind_proxy)
        self.maintenance_mode = data.get('maintenance_mode', self.maintenance_mode)
        self.memory = float(data.get('memory', self.memory))
        self.memory_overallocate = float(data.get('memory_overallocate', self.memory_overallocate))
        self.disk = data.get('disk', self.disk)
        self.disk_overallocate = float(data.get('disk_overallocate', self.disk_overallocate))
        self.upload_size = data.get('upload_size', self.upload_size)
        self.daemon_listen = data.get('daemon_listen', self.daemon_listen)
        self.daemon_sftp = data.get('daemon_sftp', self.daemon_sftp)
        self.daemon_base = data.get('daemon_base', self.daemon_base)
    
    def __repr__(self) -> str:
        return '<Node %d>' % self.id
    
    def getconfig(self):
        return NotImplemented
    
    def update(self, **kwargs):
        return NotImplemented
    
    def delete(self):
        return NotImplemented
