from ..managers.requests import RequestManager
from ..managers.servers import ApplicationServerManager
from typing import Any, Dict
from time import time


class PteroApp:
    def __init__(self, domain: str, auth: str, **kwargs) -> None:
        self.domain = domain.removesuffix('/')
        self.auth = auth
        self.options: Dict[str, Any] = {}
        self.ready_at: float = 0.0
        self.ping: float = -1.0
        self.requests: RequestManager = None
        self.servers = ApplicationServerManager(self)
    
    def __repr__(self) -> str:
        return '<PteroApp %ims>' % self.ping
    
    async def connect(self) -> bool:
        if self.requests is None:
            self.requests = RequestManager(self, 'application')
        
        await self.requests.ping()
        self.ready_at = time()
        return True
    
    async def close(self) -> None:
        if self.requests.session is None:
            return
        
        await self.requests.close()
        self.ping = -1.0
        self.ready_at = 0.0
