from typing import Optional
from .permissions import Permissions
from .types import _Http
from .util import transform


__all__ = ('Account', 'SubUser', 'User')

class Account:
    def __init__(self, http: _Http, data: dict[str,]) -> None:
        self._http = http
        self.id = data['id']
        self._patch(data)
    
    def __repr__(self) -> str:
        return '<Account id=%d>' % self.id
    
    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name
    
    def _patch(self, data: dict[str,]) -> None:
        self.username: str = data['username']
        self.email: str = data['email']
        self.first_name: str = data['first_name']
        self.last_name: str = data['last_name']
        self.language: str = data['language']
        self.admin: bool = data['admin']
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'])


class SubUser:
    def __init__(self, http: _Http, data: dict[str,]) -> None:
        self._http = http
        self.uuid: str = data['uuid']
        self.username: str = data['username']
        self.email: str = data['email']
        self.image: str | None = data.get('image')
        self.permissions = Permissions(*data['permissions'])
        self.two_factor_enabled: bool = data['2fa_enabled']
        self.created_at: str = data['created_at']
    
    def __repr__(self) -> str:
        return '<SubUser uuid=%s>' % self.uuid
    
    def __str__(self) -> str:
        return self.username
    
    def to_dict(self) -> dict[str,]:
        return transform(
            self,
            ignore=['_http'],
            map={'two_factor_enabled': '2fa_enabled'}
        )


class User:
    def __init__(self, http: _Http, data: dict[str,]) -> None:
        self._http = http
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.created_at: str = data['created_at']
        self._patch(data)
    
    def __repr__(self) -> str:
        return '<User id=%d uuid=%s>' % (self.id, self.uuid)
    
    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name
    
    def _patch(self, data: dict[str,]) -> None:
        self.external_id: Optional[str] = data.get('external_id')
        self.username: str = data['username']
        self.email: str = data['email']
        self.first_name: str = data['first_name']
        self.last_name: str = data['last_name']
        self.language: str = data['language']
        self.root_admin: bool = data['root_admin']
        self.two_factor: bool = data['2fa']
        self.updated_at: Optional[str] = data.get('updated_at')
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'], map={'two_factor': '2fa'})
