class BaseUser:
    def __init__(self, client, data: dict) -> None:
        self.client = client
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        self.id: int = data['id'] if self.id is None else self.id
        self.username: str = data['username'] if self.username is None else self.username
        self.email: str = data['email'] if self.email is None else self.email
        self.firstname: str = data['firstname'] if self.firstname is None else self.firstname
        self.lastname: str = data['lastname'] if self.lastname is None else self.lastname
        self.language: str = data['language'] if self.language is None else self.language
    
    def __str__(self) -> str:
        return self.firstname +' '+ self.lastname
    
    def __repr__(self) -> str:
        return '<%s %d>' % (self.__class__.__name__, self.id)
    
    def __dict__(self) -> dict:
        return { k: getattr(self, k) for k in dir(self) if not k.startswith('__') }


class PteroUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        self.external_id: str = data['external_id'] or self.external_id
        self.uuid: str = data['uuid']
        self.is_admin: bool = data['root_admin']
        self.tfa: bool = data['2fa']
        self.created_at: str = data['created_at']
        self.updated_at: str = data['updated_at']
        self.relationships = NotImplemented
    
    async def update(self):
        return NotImplemented
    
    async def delete(self):
        return NotImplemented


class PteroSubUser(BaseUser):
    def __init__(self, client, data: dict) -> None:
        super().__init__(client, data)
        self.__patch(data)
    
    def __patch(self, data: dict) -> None:
        super().__patch(data)
        self.uuid: str = data['uuid']
        self.image: str = data['image']
        self.enabled: bool = data['2fa_enabled']
    
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
