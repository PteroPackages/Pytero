from typing import Optional
from .util import transform


class User:
    def __init__(self, http, data: dict[str,]) -> None:
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
