from ..app.endpoints import SERVERS_GET, SERVERS_MAIN
from ..structures.users import PteroUser
from ..structures.servers import ApplicationServer
from typing import Dict, List, Optional, Union


class ApplicationServerManager:
    def __init__(self, client) -> None:
        self.client = client
        self.cache: Dict[int, ApplicationServer] = {}
    
    def __repr__(self) -> str:
        return '<AppServerManager %d>' % len(self.cache)
    
    def default_limits(self) -> Dict[str, int]:
        return {'memory': 128, 'swap': 0, 'disk': 512, 'io': 500, 'cpu': 100}
    
    def default_feature_limits(self) -> Dict[str, int]:
        return {'databases': 5, 'backups': 1}
    
    def __patch(self, data: dict) -> Union[ApplicationServer, Dict[int, ApplicationServer]]:
        if data['data']:
            res = {}
            for o in data['data']:
                s = ApplicationServer(self.client, o['attributes'])
                res[s.id] = s
            
            self.cache.update(res)
            return res
        
        s = ApplicationServer(self.client, data['attributes'])
        self.cache[s.id] = s
        return s
    
    def resolve(self, obj) -> Optional[ApplicationServer]:
        if isinstance(obj, ApplicationServer): return obj
        if type(obj) == int: return self.cache[obj]
        if type(obj) == str:
            for s in self.cache:
                if self.cache[s].name == obj:
                    return self.cache[s]
        
        return None
    
    async def fetch(self, _id: int = None, force: bool = False, include: List[str] = []):
        if _id is not None:
            if not force:
                s = self.cache.get(_id)
                if s: return s
        
        data: dict = self.client.requests.get(
            SERVERS_GET(_id) if _id is not None else SERVERS_MAIN
        )
        return self.__patch(data)
    
    def query(self, entity, filter: str = None, sort: str = None):
        return NotImplemented
    
    def create(self, user: PteroUser, **options):
        return NotImplemented
    
    def delete(self, id: int, force: bool = False):
        return NotImplemented
