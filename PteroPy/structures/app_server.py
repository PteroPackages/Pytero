from ..app.pteroapp import PteroApp
from .node import Node
from .users import PteroUser
from typing import Optional


class ApplicationServer:
    def __init__(self, client: PteroApp, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.created_at: float = data['created_at']
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.updated_at: float = data['updated_at'] or self.updated_at or None
        self.external_id: str = data['external_id'] or self.external_id
        self.name: str = data['name'] or self.name
        self.description: Optional[str] = data['description'] if len(data['description']) else None
        self.suspended: bool = data['suspended'] or self.suspended
        self.limits: dict = data['limits'] or self.limits
        self.feature_limits: dict = data['feature_limits'] or self.feature_limits
        self.user: int = data['user'] or self.user
        self.owner: Optional[PteroUser] = None
        self.node_id: int = data['node'] or self.node_id
        self.node: Optional[Node] = None
        self.allocation: int = data['allocation'] or self.allocation
        self.nest: int = data['nest'] or self.nest
    
    def __repr__(self) -> str:
        return '<%s %d>' % (self.__class__.__name__, self.id)
    
    def __dict__(self) -> dict:
        return { k: getattr(self, k) for k in dir(self) if not k.startswith('_') }
    
    async def update_details(self, **kwargs):
        return NotImplemented
    
    async def fetch_owner(self) -> Optional[PteroUser]:
        return NotImplemented
    
    async def update_build(self, build: dict):
        return NotImplemented
    
    async def update_startup(self, startup: dict):
        return NotImplemented
    
    async def suspend(self) -> bool:
        # TODO: endpoint
        return False
    
    async def unsuspend(self) -> bool:
        # TODO: endpoint
        return False
    
    async def reinstall(self) -> bool:
        # TODO: endpoint
        return False
