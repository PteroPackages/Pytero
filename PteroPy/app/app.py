from ..managers.requests import RequestManager
from ..managers.servers import ApplicationServerManager
from typing import Any, Dict
from time import time


class PteroApp:
    def __init__(self, domain: str, auth: str, **kwargs) -> None:
        self.domain = domain.removesuffix('/')
        self.auth = auth
        self.options: Dict[str, Any] = None
        
        self.ready_at: float = None
        self.ping: float = None
        
        self.requests = RequestManager(self, 'application')
        self.servers = ApplicationServerManager(self)
    
    def __repr__(self) -> str:
        return '<PteroApp %ims>' % self.ping or -1
    
    async def connect(self) -> bool:
        if self.ready_at is not None:
            raise Exception('pteroapp already connected')
        
        start = time()
        self.requests.ping()
        self.ping = time() - start
        self.ready_at = time()
        return True
    
    async def close(self) -> None:
        if self.ready_at is None:
            return
        
        await self.requests.session.close()
        self.ping = None
        self.ready_at = None
