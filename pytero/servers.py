from typing import Optional
from .types import _Http, Container, FeatureLimits, Limits
from .util import transform


__all__ = ('AppServer', 'ClientServer')

class AppServer:
    def __init__(self, http: _Http, data: dict[str,]) -> None:
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
        self.nest_id: int = data['nest']
        self.egg_id: int = data['egg']
        self.container: Container = Container(**data['container'])
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


class ClientServer:
    def __init__(self, http: _Http, data: dict[str,]) -> None:
        self._http = http
        self.uuid: str = data['uuid']
        self.identifier: str = data['identifier']
        self.internal_id: int = data['internal_id']
        self._patch(data)
    
    def __repr__(self) -> str:
        return '<ClientServer identifier=%s>' % self.identifier
    
    def __str__(self) -> str:
        return self.name
    
    def _patch(self, data: dict[str,]) -> None:
        self.server_owner: bool = data['server_owner']
        self.name: str = data['name']
        self.node: str = data['node']
        self.description: Optional[str] = data.get('description')
        self.sftp_details: dict[str,] = data['sftp_details']
        self.limits: Limits = Limits(**data['limits'])
        self.feature_limits: FeatureLimits = FeatureLimits(**data['feature_limits'])
        self.invocation: str = data['invocation']
        self.docker_image: str = data['docker_image']
        self.egg_features: Optional[list[str]] = data.get('egg_features')
        self.status: Optional[str] = data.get('status')
        self.is_suspended: bool = data['is_suspended']
        self.is_installing: bool = data['is_installing']
        self.is_transferring: bool = data['is_transferring']
    
    def _patch_relations(self) -> None:
        pass
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'])
