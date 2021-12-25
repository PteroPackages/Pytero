from .node import Node
from .users import PteroUser
from typing import Any, Dict, Optional


class ApplicationServer:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.created_at: float = data['created_at']
        self.user: Optional[PteroUser] = None
        self.node: Optional[Node] = None
        
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.updated_at: float = data.get('updated_at', 0.0)
        self.external_id: Optional[str] = data.get('external_id', None)
        self.name: str = data.get('name')
        self.description: Optional[str] = data.get('description', None)
        self.suspended: bool = data.get('suspended', False)
        self.limits: Dict[str, Any] = data.get('limits', {})
        self.feature_limits: Dict[str, Any] = data.get('feature_limits', {})
        self.user_id: int = data.get('user')
        self.node_id: int = data.get('node')
        self.allocation: int = data.get('allocation', -1)
        self.nest_id: int = data.get('nest', -1)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return '<ApplicationServer id=%d name=%s suspended=%s>' % (
            self.id, self.name, str(self.suspended)
        )
    
    def update_details(self, **kwargs):
        return NotImplemented
    
    def fetch_owner(self) -> Optional[PteroUser]:
        return NotImplemented
    
    def update_build(self, build: dict):
        return NotImplemented
    
    def update_startup(self, startup: dict):
        return NotImplemented
    
    def suspend(self) -> bool:
        # TODO: endpoint
        return False
    
    def unsuspend(self) -> bool:
        # TODO: endpoint
        return False
    
    def reinstall(self) -> bool:
        # TODO: endpoint
        return False
