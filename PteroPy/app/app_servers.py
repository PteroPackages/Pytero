from PteroPy.structures.users import PteroUser
from .pteroapp import PteroApp
from ..structures.app_server import ApplicationServer
from typing import Dict, List, Optional, Union


class ApplicationServerManager:
    def __init__(self, client: PteroApp) -> None:
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
    
    async def fetch(self, id: int = None, force: bool = False, include: List[str] = []):
        return NotImplemented
    
    async def query(self, entity, filter: str = None, sort: str = None):
        return NotImplemented
    
    async def create(self, user: PteroUser, **options):
        return NotImplemented
    
    async def delete(self, id: int, force: bool = False):
        return NotImplemented
