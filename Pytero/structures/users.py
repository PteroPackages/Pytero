from ..types import _PteroApp


class BaseUser:
    def __init__(self, client: _PteroApp, data: dict[str,]) -> None:
        self.client = client
        self._patch(data)
    
    def _patch(self, data: dict[str,]) -> None:
        self.id: int = data['id']
        self.username: str = data['username']
        self.email: str = data['email']
        self.firstname: str = data['first_name']
        self.lastname: str = data['last_name']
        self.language: str = data['language']
    
    def __str__(self) -> str:
        return self.firstname +' '+ self.lastname
    
    def __repr__(self) -> str:
        return '<%s id=%d>' % (self.__class__.__name__, self.id)


class PteroUser(BaseUser):
    def __init__(self, client: _PteroApp, data: dict[str,]) -> None:
        super().__init__(client, data)
        self._patch(data)
    
    def _patch(self, data: dict[str,]) -> None:
        super()._patch(data)
        self.external_id: str = data['external_id']
        self.uuid: str = data['uuid']
        self.is_admin: bool = data['root_admin']
        self.two_factor: bool = data['2fa']
        self.created_at: str = data['created_at']
        self.updated_at: str = data['updated_at']
        self.relationships = NotImplemented
    
    async def update(self):
        return NotImplemented
    
    async def delete(self):
        return NotImplemented


class PteroSubUser(BaseUser):
    def __init__(self, client: _PteroApp, data: dict[str,]) -> None:
        super().__init__(client, data)
        self._patch(data)
    
    def _patch(self, data: dict[str,]) -> None:
        super().__patch(data)
        self.uuid: str = data['uuid']
        self.image: str = data['image']
        self.enabled: bool = data['2fa_enabled']
    
    async def set_permissions(data: object):
        return NotImplemented


class ClientUser(BaseUser):
    def __init__(self, client: _PteroApp, data: dict[str,]) -> None:
        super().__init__(client, data)
        super()._patch(data)
        
        self.is_admin: bool = data['is_admin']
        self.tokens = []
        self.apikeys = []
    
    async def get_2fa_code(self):
        return NotImplemented
    
    async def enable_2fa(self, code: str):
        return NotImplemented
    
    async def disable_2fa(self, password: str):
        return NotImplemented
    
    async def update_email(self, email: str, password: str):
        return NotImplemented
    
    async def update_password(self, old_pass: str, new_pass: str):
        return NotImplemented
    
    async def fetch_keys(self):
        return NotImplemented
    
    async def create_key(self):
        return NotImplemented
    
    async def delete_key(self, key: str):
        return NotImplemented
