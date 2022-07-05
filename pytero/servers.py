from typing import Optional
from .types import FeatureLimits, Limits
from .util import transform


__all__ = ('AppServer')

class AppServer:
    def __init__(self, http, data: dict[str,]) -> None:
        self._http = http
        self.id: int = data['id']
        self.external_id: Optional[str] = data.get('external_id')
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.created_at: str = data['created_at']
        self._patch(data)
    
    def __repr__(self) -> str:
        return '<AppServer id=%d identifier=%s>' % (self.id, self.identifier)
    
    def __str__(self) -> str:
        return self.name
    
    def _patch(self, data: dict[str,]) -> None:
        self.name: str = data['name']
        self.description: Optional[str] = data.get('description')
        self.status: Optional[str] = data.get('status')
        self.suspended: bool = data.get('suspended', False)
        self.limits: Limits = Limits(**data['limits'])
        self.feature_limts: FeatureLimits = FeatureLimits(**data['feature_limits'])
        self.user_id: int = data['user']
        self.node_id: int = data['node']
        self.allocation_id: int = data['allocation']
        self.container: dict[str, str | int] = data['container']
        self.updated_at: Optional[str] = data.get('updated_at')
    
    def _patch_relations(self) -> None:
        pass
    
    def to_dict(self) -> dict[str,]:
        return transform(
            self,
            ignore=['_http'],
            map={
                'user_id': 'user',
                'node_id': 'node',
                'alloaction_id': 'allocation'}
        )
