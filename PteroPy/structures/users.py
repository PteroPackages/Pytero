class BaseUser:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.id: int = data['id']
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.username: str = data['username'] or self.username
        self.email: str = data['email'] or self.email
        self.firstname: str = data['firstname'] or self.firstname
        self.lastname: str = data['lastname'] or self.lastname
        self.language: str = data['language'] or self.language
    
    def __str__(self) -> str:
        return self.firstname +' '+ self.lastname
    
    def __repr__(self) -> str:
        return '<%s %d>' % (self.__class__.__name__, self.id)
    
    def __dict__(self) -> dict:
        return { k: getattr(self, k) for k in dir(self) if not k.startswith('_') }


class PteroUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        self.uuid: str = data['uuid']
        self.created_at: str = data['created_at']
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        self.external_id: str = data['external_id'] or self.external_id
        self.is_admin: bool = data['root_admin'] or self.is_admin
        self.tfa: bool = data['2fa'] or self.tfa
        self.updated_at: str = data['updated_at'] or self.updated_at
        self.relationships = NotImplemented
    
    async def update(self):
        return NotImplemented
    
    async def delete(self):
        return NotImplemented


class PteroSubUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        self.uuid: str = data['uuid']
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        self.image: str = data['image'] or self.image
        self.enabled: bool = data['2fa_enabled'] or self.enabled
    
    async def set_permissions(data: object):
        return NotImplemented


class ClientUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        super().__patch(data)
        
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
