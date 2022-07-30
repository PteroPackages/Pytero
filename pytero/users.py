from typing import Optional
from .permissions import Permissions
from .servers import AppServer
from .types import _Http, APIKey, Activity, SSHKey
from .util import transform


__all__ = ('Account', 'SubUser', 'User')


class Account:
    def __init__(self, http, data: dict[str,]) -> None:
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
    
    def get_two_factor(self) -> str:
        return self._http.get_account_two_factor()
    
    def enable_two_factor(self, code: int, /) -> list[str]:
        return self._http.enable_account_two_factor(code)
    
    def disable_two_factor(self, password: str, /) -> None:
        return self._http.disable_account_two_factor(password)
    
    async def update_email(self, email: str, password: str) -> None:
        await self._http.update_account_email(email, password)
        self.email = email
    
    def update_password(self, old: str, new: str) -> None:
        return self._http.update_account_password(old, new)
    
    def get_activities(self) -> list[Activity]:
        return self._http.get_account_activities()
    
    def get_api_keys(self) -> list[APIKey]:
        return self._http.get_api_keys()
    
    def get_ssh_keys(self) -> list[SSHKey]:
        return self._http.get_ssh_keys()


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
            map={'two_factor_enabled': '2fa_enabled'})


class User:
    def __init__(self, http, data: dict[str,]) -> None:
        self._http = http
        self.id: int = data['id']
        self.uuid: str = data['uuid']
        self.created_at: str = data['created_at']
        self._patch(data)
        self._patch_relations(data.get('relationships'))
    
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
        self.servers: list[AppServer] = []
    
    def _patch_relations(self, data: dict[str,] | None) -> None:
        if data is None:
            return
        
        if 'servers' in data:
            for datum in data['servers']['data']:
                self.servers.append(AppServer(self._http, datum['attributes']))
    
    def to_dict(self) -> dict[str,]:
        return transform(self, ignore=['_http'], maps={'two_factor': '2fa'})
    
    async def update(
        self,
        *,
        email: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        password: str = None,
        external_id: str = None,
        root_admin: bool = None
    ) -> None:
        email = email or self.email
        username = username or self.username
        first_name = first_name or self.first_name
        last_name = last_name or self.last_name
        external_id = external_id or self.external_id
        if root_admin is None:
            root_admin = self.root_admin
        
        data: User = await self._http.update_user(
            self.id,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            external_id=external_id,
            root_admin=root_admin)
        
        self._patch(data.to_dict())
